import json
import sys
import os
import re
import asyncio
import threading
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from http.server import BaseHTTPRequestHandler, HTTPServer

from fastmcp import FastMCP
from pydantic import BaseModel
import websockets
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================
# Configuration
# =========================

class Settings:
    def __init__(self):
        self.ws_port = int(os.environ.get("WS_PORT", 5000))
        self.http_port = int(os.environ.get("HTTP_PORT", 8000))
        self.persistence_file = os.environ.get("PERSISTENCE_FILE", "diagrams.json")
        self.max_elements = int(os.environ.get("MAX_ELEMENTS", 1000))
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")
        self.rate_limit_per_minute = int(os.environ.get("RATE_LIMIT", 60))

settings = Settings()

# Print settings for debugging
print(f"[CONFIG] WS_PORT: {settings.ws_port}, HTTP_PORT: {settings.http_port}, PERSISTENCE_FILE: {settings.persistence_file}", file=sys.stderr)

# =========================
# Logging setup
# =========================

# Create logs directory if it doesn't exist
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Create log filename with timestamp
from datetime import datetime
log_filename = f"{logs_dir}/mcp_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(log_filename)
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"Server configuration: WS_PORT={settings.ws_port}, HTTP_PORT={settings.http_port}, PERSISTENCE_FILE={settings.persistence_file}")

# =========================
# Rate limiting
# =========================

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = {}
        self.lock = threading.Lock()
    
    def is_allowed(self, key: str = "default") -> bool:
        now = datetime.now().timestamp()
        with self.lock:
            if key not in self.calls:
                self.calls[key] = []
            
            # Remove old calls outside the time window
            self.calls[key] = [call for call in self.calls[key] if now - call < self.time_window]
            
            if len(self.calls[key]) < self.max_calls:
                self.calls[key].append(now)
                return True
            return False

rate_limiter = RateLimiter(settings.rate_limit_per_minute)

# =========================
# Data models
# =========================

class DiagramElement(BaseModel):
    id: str
    type: str  # "rectangle" | "ellipse" | "diamond" | "arrow" | "text"
    x: float
    y: float
    width: Optional[float] = None
    height: Optional[float] = None
    text: Optional[str] = None
    fromId: Optional[str] = None  # For arrows
    toId: Optional[str] = None    # For arrows
    label: Optional[str] = None   # For edge labels
    backgroundColor: Optional[str] = "transparent"
    strokeColor: Optional[str] = "#000000"
    fillStyle: Optional[str] = "hachure"


class DiagramScene(BaseModel):
    elements: List[DiagramElement]


# =========================
# Thread-safe in-memory store with persistence
# =========================

class Store:
    def __init__(self, file_path: str = "diagrams.json"):
        self._lock = threading.Lock()
        self.elements: List[DiagramElement] = []
        self.file_path = file_path
        self.load_from_disk()

    def load_from_disk(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.elements = [DiagramElement(**el) for el in data]
                logger.info(f"Loaded {len(self.elements)} elements from {self.file_path}")
                print(f"[STORE] Loaded {len(self.elements)} elements from {self.file_path}", file=sys.stderr)
        except FileNotFoundError:
            logger.info(f"No existing file {self.file_path}, starting fresh")
            print(f"[STORE] No existing file {self.file_path}, starting fresh", file=sys.stderr)
        except Exception as e:
            print(f"[STORE] Error loading from disk: {e}", file=sys.stderr)

    def save_to_disk(self):
        try:
            with self._lock:
                with open(self.file_path, 'w') as f:
                    json.dump([el.model_dump() for el in self.elements], f, indent=2)
                print(f"[STORE] Saved {len(self.elements)} elements to {self.file_path}", file=sys.stderr)
        except Exception as e:
            print(f"[STORE] Error saving to disk: {e}", file=sys.stderr)

    def get_scene(self) -> DiagramScene:
        with self._lock:
            # return a copy to avoid external mutation
            return DiagramScene(elements=list(self.elements))

    def set_elements(self, elements: List[DiagramElement]):
        with self._lock:
            self.elements = list(elements)
            self.save_to_disk()

    def add_element(self, element: DiagramElement):
        with self._lock:
            self.elements.append(element)
            self.save_to_disk()

    def clear(self):
        with self._lock:
            self.elements = []
            self.save_to_disk()


store = Store(settings.persistence_file)


def extract_edges(description: str) -> List[tuple]:
    """Extract edges from natural language description with enhanced patterns."""
    edges = []
    
    # Enhanced patterns for connections
    patterns = [
        r'(\w+)\s+connects?\s+to\s+(\w+)',
        r'(\w+)\s+which\s+\w+\s+(\w+)',
        r'(\w+)\s+linked\s+to\s+(\w+)',
        r'(\w+)\s+points\s+to\s+(\w+)',
        r'(\w+)\s+flows\s+to\s+(\w+)',
        r'(\w+)\s+goes\s+to\s+(\w+)',
        r'(\w+)\s+sends\s+to\s+(\w+)',
        r'(\w+)\s+calls\s+(\w+)',
        r'(\w+)\s+interacts?\s+with\s+(\w+)',
        r'(\w+)\s+communicates?\s+with\s+(\w+)',
        r'(\w+)\s+depends\s+on\s+(\w+)',
        r'(\w+)\s+uses\s+(\w+)',
        r'(\w+)\s+accesses\s+(\w+)',
        r'(\w+)\s+queries\s+(\w+)',
        r'(\w+)\s+writes?\s+to\s+(\w+)',
        r'(\w+)\s+reads?\s+from\s+(\w+)',
        r'(\w+)\s+authenticates?\s+with\s+(\w+)',
        r'(\w+)\s+logs?\s+in\s+to\s+(\w+)',
        r'(\w+)\s+signs?\s+up\s+with\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        for match in matches:
            # Filter out pronouns and articles
            exclude_words = {'which', 'that', 'who', 'what', 'where', 'when', 'why', 'how', 'the', 'a', 'an', 'and', 'or', 'but', 'so', 'because', 'although', 'while', 'if', 'then', 'else'}
            u, v = match[0].strip(), match[1].strip()
            if u.lower() not in exclude_words and v.lower() not in exclude_words:
                edges.append((u, v))
    
    # Handle arrow notation with more variations
    arrow_patterns = [
        r'(\w+)\s*->\s*(\w+)',
        r'(\w+)\s*→\s*(\w+)',  # Unicode arrow
        r'(\w+)\s*-->\s*(\w+)',
        r'(\w+)\s*<-\s*(\w+)',
        r'(\w+)\s*<--\s*(\w+)',
    ]
    
    for pattern in arrow_patterns:
        matches = re.findall(pattern, description)
        for match in matches:
            edges.append((match[0].strip(), match[1].strip()))
    
    # Handle multi-step chains like "A -> B -> C"
    chain_matches = re.findall(r'(\w+)\s*->\s*(\w+)\s*->\s*(\w+)', description)
    for match in chain_matches:
        edges.extend([(match[0].strip(), match[1].strip()), (match[1].strip(), match[2].strip())])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_edges = []
    for edge in edges:
        edge_tuple = tuple(edge)
        if edge_tuple not in seen:
            seen.add(edge_tuple)
            unique_edges.append(edge)
    
    print(f"[EDGES] Extracted {len(unique_edges)} edges: {unique_edges}", file=sys.stderr)
    return unique_edges


def get_shape(label: str) -> str:
    """Determine shape based on label content."""
    label_lower = label.lower()
    if any(word in label_lower for word in ["database", "db", "storage", "data"]):
        return "ellipse"
    if any(word in label_lower for word in ["decision", "if", "condition", "switch"]):
        return "diamond"
    if any(word in label_lower for word in ["process", "action", "task"]):
        return "rectangle"  # default
    return "rectangle"


# =========================
# WebSocket layer
# =========================

active_connections: set[websockets.WebSocketServerProtocol] = set()
ws_loop: Optional[asyncio.AbstractEventLoop] = None  # set when WS server starts


def validate_elements(elements: List[DiagramElement]) -> List[DiagramElement]:
    """Filter out invalid elements (especially bad arrows)."""
    valid: List[DiagramElement] = []
    for el in elements:
        try:
            if el.type == "arrow":
                if not el.fromId or not el.toId:
                    print(f"[WS] Skipping invalid arrow {el.id} (missing fromId/toId)", file=sys.stderr)
                    continue
            valid.append(el)
        except Exception as e:
            print(f"[WS] Skipping malformed element: {e}", file=sys.stderr)
    return valid


async def broadcast_scene() -> None:
    """Send the current scene to all connected WebSocket clients."""
    try:
        if not active_connections:
            print("[WS] No active connections to broadcast to", file=sys.stderr)
            return

        try:
            scene = store.get_scene()
            elements = validate_elements(scene.elements)
            scene_dict = {"elements": [el.model_dump() for el in elements]}
        except Exception:
            # Pydantic v1 fallback if needed
            scene = store.get_scene()
            elements = validate_elements(scene.elements)
            scene_dict = {"elements": [el.dict() for el in elements]}

        msg = {
            "type": "scene_update",
            "scene": scene_dict,
        }
        msg_json = json.dumps(msg)

        print(
            f"[WS] Broadcasting scene with {len(scene_dict['elements'])} elements "
            f"to {len(active_connections)} clients",
            file=sys.stderr,
        )
        sys.stderr.flush()

        disconnected: set[websockets.WebSocketServerProtocol] = set()

        for ws in active_connections.copy():
            try:
                await ws.send(msg_json)
                print(f"[WS] Sent update to client {ws.remote_address}", file=sys.stderr)
                sys.stderr.flush()
            except Exception as e:
                print(f"[WS] Failed to send to client {ws.remote_address}: {e}", file=sys.stderr)
                sys.stderr.flush()
                disconnected.add(ws)

        for ws in disconnected:
            active_connections.discard(ws)
        if disconnected:
            print(f"[WS] Removed {len(disconnected)} disconnected clients", file=sys.stderr)
            sys.stderr.flush()
    except Exception as e:
        print(f"[WS] broadcast_scene fatal error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()


def broadcast_future_callback(future):
    try:
        future.result()
    except Exception as e:
        print(f"[WS] Broadcast coroutine failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)


def schedule_broadcast() -> None:
    """
    Safe cross-thread broadcast:
    - Called from MCP tools (FastMCP thread) or HTTP demo thread.
    - Schedules broadcast_scene() on the running websocket event loop.
    """
    global ws_loop
    if ws_loop is None or not ws_loop.is_running():
        print("[WS] schedule_broadcast called but ws_loop is not running", file=sys.stderr)
        return

    try:
        future = asyncio.run_coroutine_threadsafe(broadcast_scene(), ws_loop)
        future.add_done_callback(broadcast_future_callback)
        print("[WS] Broadcast scheduled", file=sys.stderr)
        sys.stderr.flush()
    except Exception as e:
        print(f"[WS] Failed to schedule broadcast: {e}", file=sys.stderr)
        sys.stderr.flush()


async def ws_handler(websocket, path=None):
    logger.info(f"New WebSocket connection from {websocket.remote_address}")
    print(f"[WS] New WebSocket connection from {websocket.remote_address}", file=sys.stderr)
    active_connections.add(websocket)
    print(f"[WS] Total active connections: {len(active_connections)}", file=sys.stderr)

    # Send initial state
    try:
        scene = store.get_scene()
        elements = validate_elements(scene.elements)
        scene_dict = {"elements": [el.model_dump() for el in elements]}
    except Exception:
        scene = store.get_scene()
        elements = validate_elements(scene.elements)
        scene_dict = {"elements": [el.dict() for el in elements]}

    initial = {"type": "scene_update", "scene": scene_dict}
    await websocket.send(json.dumps(initial))
    print(f"[WS] Sent initial state with {len(scene_dict['elements'])} elements", file=sys.stderr)

    try:
        async for message in websocket:
            # optional: echo logs
            print(f"[WS] Received message from client: {message}", file=sys.stderr)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"[WS] WebSocket closed: {e}", file=sys.stderr)
    finally:
        active_connections.discard(websocket)
        print(f"[WS] Connection removed, {len(active_connections)} remaining", file=sys.stderr)


async def start_ws_server():
    global ws_loop
    ws_loop = asyncio.get_running_loop()
    print(f"[WS] Starting WebSocket server on 127.0.0.1:{settings.ws_port}", file=sys.stderr)

    async with websockets.serve(ws_handler, "127.0.0.1", settings.ws_port):
        print(f"[WS] WebSocket server is listening on ws://127.0.0.1:{settings.ws_port}", file=sys.stderr)
        await asyncio.Future()  # run forever


def run_ws_server():
    try:
        asyncio.run(start_ws_server())
    except Exception as e:
        print(f"[WS] WebSocket server crashed: {e}", file=sys.stderr)


# =========================
# FastMCP server
# =========================

app = FastMCP("Excalidraw MCP Server")


@app.tool()
def generate_diagram(description: str) -> str:
    """
    Generate a diagram from a description.
    Supports natural language descriptions with various connection patterns.
    Automatically detects shapes based on content (database=ellipse, decision=diamond).
    Examples:
    - "User connects to API which interacts with Database"
    - "Client sends request to Server which calls Database"
    - A -> B -> C
    - Complex branching: "API connects to DB and Cache"
    """
    try:
        # Rate limiting
        if not rate_limiter.is_allowed():
            return "Error: Rate limit exceeded. Please wait before making another request."
        
        # Input validation
        if not description or not description.strip():
            return "Error: Description cannot be empty"
        
        if len(description) > 10000:  # Reasonable limit
            return "Error: Description too long (max 10000 characters)"
        
        # Sanitize input - remove potentially harmful characters
        description = re.sub(r'[^\w\s\-.,!?()\'\"]+', '', description)
        
        logger.info(f"generate_diagram called with: {description}")
        print(f"[MCP] generate_diagram called with: {description}", file=sys.stderr)
        store.clear()

        # Extract edges from description
        edges = extract_edges(description)
        
        # Build nodes from edges
        nodes = {}
        for u, v in edges:
            if u not in nodes:
                nodes[u] = f"node-{len(nodes)}"
            if v not in nodes:
                nodes[v] = f"node-{len(nodes)}"

        new_elements: List[DiagramElement] = []
        
        # Simple grid layout
        # Assign levels using BFS
        levels = {}
        if not nodes:
            return "Empty diagram"
            
        start_node = list(nodes.keys())[0] # Heuristic: start with first mentioned
        queue = [(start_node, 0)]
        visited = {start_node}
        levels[start_node] = 0
        
        # Build adjacency list for BFS
        adj = {n: [] for n in nodes}
        for u, v in edges:
            adj[u].append(v)
            
        while queue:
            u, level = queue.pop(0)
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    levels[v] = level + 1
                    queue.append((v, level + 1))
                    
        # Handle disconnected components
        for n in nodes:
            if n not in visited:
                levels[n] = 0 # Just put them at start
                
        # Group by level to determine Y position
        level_groups = {}
        for n, lvl in levels.items():
            if lvl not in level_groups:
                level_groups[lvl] = []
            level_groups[lvl].append(n)
            
        # Create Node Elements
        palette = [
            {"bg": "#ffc9c9", "stroke": "#c92a2a"},  # Red
            {"bg": "#b2f2bb", "stroke": "#2b8a3e"},  # Green
            {"bg": "#a5d8ff", "stroke": "#1864ab"},  # Blue
            {"bg": "#ffec99", "stroke": "#e67700"},  # Yellow
            {"bg": "#eebefa", "stroke": "#862e9c"},  # Grape
        ]
        
        node_positions = {}
        node_sizes = {}
        
        for label in nodes:
            text_len = len(label)
            width = max(150, text_len * 8 + 40)  # Approximate character width
            height = 60
            node_sizes[label] = (width, height)
        
        max_width_per_level = {}
        for lvl, group in level_groups.items():
            max_width_per_level[lvl] = max(node_sizes[label][0] for label in group) if group else 150
        
        for lvl, group in level_groups.items():
            level_width = max_width_per_level[lvl]
            x_start = 150
            y_spacing = 200
            for idx, label in enumerate(group):
                node_id = nodes[label]
                width, height = node_sizes[label]
                x = x_start + (lvl * (level_width + 100))  # Space between levels
                y = 150 + (idx * y_spacing)
                node_positions[label] = (x, y)
                
                style = palette[len(new_elements) % len(palette)]
                
                new_elements.append(
                    DiagramElement(
                        id=node_id,
                        type=get_shape(label),
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        text=label,
                        backgroundColor=style["bg"],
                        strokeColor=style["stroke"],
                        fillStyle="solid",
                    )
                )

        # Create Edge Elements
        for i, (u, v) in enumerate(edges):
            arrow_id = f"arrow-{i}"
            new_elements.append(
                DiagramElement(
                    id=arrow_id,
                    type="arrow",
                    x=0,
                    y=0,
                    fromId=nodes[u],
                    toId=nodes[v],
                )
            )

        # Validate element count
        if len(new_elements) > settings.max_elements:
            return f"Error: Too many elements generated ({len(new_elements)} > {settings.max_elements})"

        store.set_elements(new_elements)
        logger.info(f"Created {len(new_elements)} elements")
        print(f"[MCP] Created {len(new_elements)} elements", file=sys.stderr)
        schedule_broadcast()
        return f"Generated diagram with {len(new_elements)} elements."
    except Exception as e:
        print(f"[MCP] generate_diagram failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return "Error: failed to generate diagram"


@app.tool()
def create_element(type: str, text: str, x: float, y: float) -> str:
    """Add a single element to the diagram."""
    try:
        print(f"[MCP] create_element {type} '{text}' at ({x}, {y})", file=sys.stderr)
        el_id = f"el-{int(datetime.now().timestamp() * 1000)}"
        element = DiagramElement(
            id=el_id,
            type=type,
            text=text,
            x=x,
            y=y,
            width=120,
            height=60,
        )
        store.add_element(element)
        schedule_broadcast()
        return f"Created element {el_id}"
    except Exception as e:
        print(f"[MCP] create_element failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return "Error: failed to create element"


@app.tool()
def connect_elements(fromId: str, toId: str, label: Optional[str] = None) -> str:
    """Connect two existing elements with an arrow."""
    try:
        print(f"[MCP] connect_elements {fromId} -> {toId}", file=sys.stderr)
        element = DiagramElement(
            id=f"arrow-{int(datetime.now().timestamp() * 1000)}",
            type="arrow",
            x=0,
            y=0,
            fromId=fromId,
            toId=toId,
            label=label,
        )
        store.add_element(element)
        schedule_broadcast()
        return "Connected elements."
    except Exception as e:
        print(f"[MCP] connect_elements failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return "Error: failed to connect elements"


@app.tool()
def clear_scene() -> str:
    """Clear the entire canvas."""
    try:
        print("[MCP] clear_scene called", file=sys.stderr)
        store.clear()
        schedule_broadcast()
        return "Scene cleared."
    except Exception as e:
        print(f"[MCP] clear_scene failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return "Error: failed to clear scene"


def start_mcp_server():
    print("[MCP] Starting MCP server (stdio)", file=sys.stderr)
    app.run()  # stdio is default; perfect for Claude Desktop


# =========================
# Demo HTTP endpoint for testing
# =========================

def start_demo_http_server():
    class DemoHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            sys.stderr.write("[DEMO HTTP] " + (format % args) + "\n")

        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                health_data = {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "elements_count": len(store.get_scene().elements),
                    "active_connections": len(active_connections),
                    "ws_port": settings.ws_port,
                    "persistence_file": settings.persistence_file
                }
                self.wfile.write(json.dumps(health_data).encode())
                return
            elif self.path != "/demo":
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            try:
                parts = [
                    "User",
                    "API Gateway",
                    "Auth Service",
                    "Orders Service",
                    "Payments Service",
                    "Inventory Service",
                    "Database",
                ]
                new_elements: List[DiagramElement] = []
                x = 100
                y = 100
                for idx, label in enumerate(parts):
                    nid = f"demo-node-{idx}"
                    new_elements.append(
                        DiagramElement(
                            id=nid,
                            type="rectangle",
                            x=x,
                            y=y,
                            width=150,
                            height=60,
                            text=label,
                        )
                    )
                    if idx > 0:
                        aid = f"demo-arrow-{idx}"
                        new_elements.append(
                            DiagramElement(
                                id=aid,
                                type="arrow",
                                x=0,
                                y=0,
                                fromId=f"demo-node-{idx-1}",
                                toId=nid,
                            )
                        )
                    x += 200

                store.set_elements(new_elements)
                schedule_broadcast()
                sys.stderr.write(
                    f"[DEMO HTTP] Demo scene with {len(new_elements)} elements queued\n"
                )

                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    f"Demo scene with {len(new_elements)} elements queued".encode(
                        "utf-8"
                    )
                )
            except Exception as e:
                sys.stderr.write(f"[DEMO HTTP] Error: {e}\n")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal error")

    try:
        server = HTTPServer(("127.0.0.1", settings.http_port), DemoHandler)
        sys.stderr.write(
            f"[DEMO HTTP] Demo HTTP server listening on http://127.0.0.1:{settings.http_port}/demo\n"
        )
        server.serve_forever()
    except Exception as e:
        sys.stderr.write(f"[DEMO HTTP] Failed to start: {e}\n")


# =========================
# Main entrypoint
# =========================

if __name__ == "__main__":
    print("Starting Excalidraw MCP Server...", file=sys.stderr)

    # Start MCP server in background (stdio for Claude Desktop)
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()
    print("[MAIN] MCP server thread started", file=sys.stderr)

    # Demo HTTP server (optional)
    demo_thread = threading.Thread(target=start_demo_http_server, daemon=True)
    demo_thread.start()

    # WebSocket server in main thread (blocks)
    run_ws_server()
