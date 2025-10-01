from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """_summary_
    Add two numbers

    """

    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """_summary_
    multiply two numbers 
    """

    
    return a*b  

@mcp.tool()
def sub(a:int,b:int)->int:
    """
    subtract two numbers
    """

    return a-b

'''
transport="stdio" argutemt tells the server to:
use standard input/output (stdin and stdout) to receive and respond to tool function calls.

'''




if __name__=="__main__":
    mcp.run(transport="stdio")



# In the context of MCP (Model Context Protocol), "transports" refer to the communication methods used between an MCP server (like your mathserver.py) and an MCP client (typically an AI assistant or application). They define how messages (tool calls, responses, etc.) are exchanged.

# Based on your code and common MCP implementations:

# ## stdio (Standard Input/Output)
# - What it is: Uses standard input (`stdin`) and standard output (`stdout`) for communication
# - How it works: The server reads JSON-RPC messages from stdin and writes responses to stdout
# - Use case: Local communication, typically when the MCP server runs as a subprocess of the client
# - Your code example: `mcp.run(transport="stdio")` - this is the most common transport for development and local testing

# ## streamable-http
# - What it is: HTTP-based transport that supports streaming responses
# - How it works: Uses HTTP requests/responses with streaming capabilities for real-time communication
# - Use case: Network-based communication, useful for remote servers or web deployments
# - Advantages: Allows for persistent connections and streaming data, better for long-running operations

# ## Other Common Transports
# - sse (Server-Sent Events): For push-based communication from server to client
# - websocket: Bidirectional real-time communication

# In your mathserver.py, you're using `transport="stdio"` which is perfect for local development. When deploying to production or integrating with web applications, you might switch to `streamable-http` or other network transports depending on your infrastructure needs.

# The transport choice affects how the MCP client connects to and interacts with your math tools (add, multiply functions).    




'''
# Key Differences

| Aspect | stdio | streamable-http |
|--------|-------|-----------------|
| Communication | Standard input/output streams | HTTP protocol with streaming |
| Connection | Local subprocess communication | Network-based (HTTP requests) |
| Persistence | Single request-response per invocation | Persistent connection with streaming |
| Performance | Very low overhead, fastest | Higher overhead but supports streaming |
| Security | Local only (process isolation) | Network security considerations needed |

## When to Use Each

### Use `stdio` when:
- Local development and testing - Perfect for building and debugging your MCP server
- Running as a subprocess - When your MCP server is launched by another application
- Simple integrations - For tools that don't need network access
- Development environments - VS Code extensions, CLI tools, local AI assistants
- Resource-constrained environments - Minimal memory/CPU overhead

### Use `streamable-http` when:
- Production deployments - Serving MCP tools over a network
- Web applications - Integrating with web-based AI assistants or chatbots
- Remote access - When clients need to connect from different machines
- Streaming responses - For long-running operations or real-time data
- Scalable architectures - Multiple clients connecting to the same server
- Cloud deployments - Running MCP servers on remote infrastructure

## Practical Examples

stdio example (your current setup):
```python
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Local subprocess communication
```

streamable-http example:
```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

## Recommendation

Start with `stdio` for development - it's simpler and faster for testing. Switch to `streamable-http` when you need to deploy your MCP server for broader access or integrate with web applications. Many MCP implementations support both transports, allowing you to use stdio locally and HTTP in production.
'''