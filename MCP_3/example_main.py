# main.py
import json
import sys
from typing import Any, Dict
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, Resource, Prompt, CallToolResult, ResourceContents, TextContent


# ================================
# 1. Initialize MCP Server
# ================================
@asynccontextmanager
async def lifespan(mcp: FastMCP) -> AsyncIterator[None]:
    print("MCP Server STARTED: my-python-mcp-server v1.0.0", file=sys.stderr)
    print("Available: add_numbers, echo, mcp://greeting, mcp://info", file=sys.stderr)
    try:
        yield
    finally:
        print("MCP Server SHUT DOWN", file=sys.stderr)

mcp = FastMCP("my-python-mcp-server", lifespan=lifespan)