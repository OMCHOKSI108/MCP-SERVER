from mcp.server.fastmcp import FastMCP
# 

mcp = FastMCP("Weather")

@mcp.tool()
async def get_location(location:str) -> str:
    """
    get the weather location 

    """

    return "Its always raining in South gujarat in August"





# Module providing a minimal FastMCP "Weather" tool.
# This module registers a single asynchronous tool, get_location(location: str) -> str,
# which returns a short human-readable message about the given location.
# Functions:
#     get_location(location: str) -> str
#         Async tool that accepts a location name and returns a string message.
# Parameters:
#     location (str): Name of the location to query.
# Returns:
#     str: A short message describing the weather/location.
# Notes on transport "streamable-http":
#     The call mcp.run(transport="streamable-http") starts the MCP server using an
#     HTTP transport mode that streams responses to clients incrementally instead of
#     sending one complete response at the end of processing. This is commonly
#     implemented with chunked transfer encoding or Server-Sent Events (SSE), and is
#     useful when the tool produces progressive output (for example, streaming model
#     tokens or partial results). The exact details (SSE vs chunked responses, event
#     framing, client integration) depend on the FastMCP/transport implementation,
#     but in general "streamable-http" allows clients to begin receiving data as it
#     is produced rather than waiting for the full response.


if __name__=="__main__":
    mcp.run(transport="streamable-http")
