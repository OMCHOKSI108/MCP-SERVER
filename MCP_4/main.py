#!/usr/bin/env python3
"""
Main entry point for the AI Workflow Orchestrator MCP server.
"""

from src.server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
