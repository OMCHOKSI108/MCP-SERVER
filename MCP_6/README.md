# Excalidraw MCP System

A production-ready Model Context Protocol (MCP) server for generating and collaborating on diagrams in real-time using Excalidraw.

## Features

- **Real-time Collaboration**: WebSocket-based live diagram synchronization
- **Persistent Storage**: Diagrams saved to JSON file with automatic recovery
- **Advanced NLP**: Enhanced natural language processing for diagram generation
- **Rate Limiting**: Built-in protection against abuse
- **Health Monitoring**: RESTful health check endpoint
- **Configurable**: Environment-based configuration
- **Robust Error Handling**: Comprehensive validation and recovery

## Prerequisites
- Node.js 20+
- Python 3.12+
- npm or pnpm

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WS_PORT` | 5000 | WebSocket server port |
| `HTTP_PORT` | 8000 | HTTP health/demo server port |
| `PERSISTENCE_FILE` | diagrams.json | File to store diagram data |
| `MAX_ELEMENTS` | 1000 | Maximum elements per diagram |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `RATE_LIMIT` | 60 | Requests per minute limit |

## Logging

The server automatically creates timestamped log files in the `logs/` directory:

- Log files are named `mcp_server_YYYYMMDD_HHMMSS.log`
- Logs include both console output and file storage
- Log level can be configured via `LOG_LEVEL` environment variable
- The `logs/` directory is automatically created and ignored by git

## 1. Setup Server
```bash
pip install -r requirements.txt
# or
pip install fastmcp uvicorn pydantic websockets
```

## 2. Setup Client
```bash
cd client
npm install
npm run dev
```
Open http://localhost:5173 to see the canvas.

## 3. Configure Claude Desktop

Create or update your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "excalidraw": {
      "command": "cmd",
      "args": ["/c", "cd /d D:\\WORKSPACE\\MCP\\MCP_6 && venv\\Scripts\\activate && python server.py"],
      "env": {
        "WS_PORT": "5000",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

Restart Claude Desktop.

## Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Demo Diagram
```bash
curl http://localhost:8000/demo
```

### Claude Commands
Ask Claude:
- "Generate a diagram showing User -> API -> Database"
- "Create a flowchart of login process"
- "Show me a microservices architecture"

## API Reference

### MCP Tools
- `generate_diagram(description)`: Generate diagram from natural language
- `create_element(type, text, x, y)`: Add individual element
- `connect_elements(fromId, toId, label)`: Connect two elements
- `clear_scene()`: Clear the canvas

### Supported Patterns
- Direct connections: "A connects to B"
- Arrows: "A -> B -> C"
- Complex relationships: "API interacts with Database and Cache"
- Multi-word nodes: "API Gateway", "User Service"

## Troubleshooting

### Common Issues
1. **Diagrams not persisting**: Check write permissions on `diagrams.json`
2. **WebSocket connection fails**: Verify `WS_PORT` matches frontend
3. **Rate limited**: Wait 1 minute or increase `RATE_LIMIT`
4. **Large diagrams fail**: Reduce `MAX_ELEMENTS` or simplify description

### Logs
Check `server.log` for detailed error information.