from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import database
import llm_service
import asyncio
import logging
from typing import Any, Optional
import sys
import json
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-web-scraper")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    database.init_db()
    logger.info("Database initialized on startup")
    yield
    # Shutdown (if needed)
    logger.info("Application shutting down")

# Create a FastAPI app instance
app = FastAPI(
    title="MCP Web Scraping Agent",
    description="A Model Context Protocol (MCP) compatible web scraping agent with AI capabilities",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    """ A default endpoint to welcome users to your API. """
    return {
        "message": "Welcome to the MCP Web Scraping Agent API",
        "version": "1.0.0",
        "features": ["FastAPI REST endpoints", "MCP protocol support", "AI-powered content analysis"],
        "endpoints": {
            "scrape": "/scrape/",
            "data": "/data/", 
            "agent_query": "/agent/query/",
            "mcp_tools": "/mcp/tools/",
            "docs": "/docs"
        }
    }

@app.post("/scrape/")
async def scrape_website(url: str):
    """
    Scrapes a URL with requests + BeautifulSoup and saves the content to the database.
    """
    try:
        # Fetch the content from the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content - convert to markdown-like format
        page_text = soup.get_text(separator='\n', strip=True)

        # --- Save the result to the database ---
        database.add_scraped_data(url=url, content=page_text)
        # -------------------------------------------

        return {
            "url": url,
            "message": "Content successfully scraped and stored.",
            "scraped_content_markdown": page_text
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve the URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/data/")
async def view_stored_data():
    """
    A new endpoint to view all the data stored in the agent's memory.
    """
    stored_data = database.get_all_scraped_data()
    return {"agent_memory": stored_data}

@app.post("/agent/query/")
async def agent_query(request: dict):
    """
    The primary intelligence endpoint. Checks memory, scrapes if needed, and queries Gemini.
    Expects JSON: {"url": "https://example.com", "prompt": "Summarize this page"}
    """
    url = request.get("url")
    prompt = request.get("prompt")

    if not url or not prompt:
        raise HTTPException(status_code=400, detail="Both 'url' and 'prompt' are required.")

    # Check if content is already in memory
    stored_data = database.get_all_scraped_data()
    content = None
    for item in stored_data:
        if item["url"] == url:
            # Assuming we store content, but in get_all_scraped_data we only select id, url, scraped_at
            # Need to modify to get content too
            content = database.get_content_by_url(url)
            break

    # If not in memory, scrape it
    if content is None:
        try:
            # Fetch the content from the URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            content = soup.get_text(separator='\n', strip=True)
            
            if content:
                database.add_scraped_data(url=url, content=content)
            else:
                raise HTTPException(status_code=404, detail="Could not extract content from the URL.")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

    # Query the LLM with the context and prompt
    response = llm_service.query_llm(context=content, prompt=prompt)

    return {
        "url": url,
        "prompt": prompt,
        "agent_response": response
    }

# ====== MCP Compatible Endpoints ======

@app.get("/mcp/tools/")
async def list_mcp_tools():
    """
    List available MCP tools for integration with AI applications.
    """
    tools = [
        {
            "name": "scrape_website",
            "description": "Scrape content from a website and store it in memory",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to scrape"}
                },
                "required": ["url"]
            }
        },
        {
            "name": "query_agent", 
            "description": "Ask the AI agent a question about scraped content",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to analyze"},
                    "prompt": {"type": "string", "description": "The question or prompt for the AI agent"}
                },
                "required": ["url", "prompt"]
            }
        },
        {
            "name": "get_stored_data",
            "description": "Retrieve all stored scraped data from memory", 
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "search_content",
            "description": "Search for specific content in stored data",
            "input_schema": {
                "type": "object", 
                "properties": {
                    "query": {"type": "string", "description": "Search query to find relevant content"}
                },
                "required": ["query"]
            }
        }
    ]
    return {"tools": tools}

@app.post("/mcp/call_tool/")
async def call_mcp_tool(request: dict):
    """
    Execute MCP tools for AI application integration.
    Expected format: {"name": "tool_name", "arguments": {...}}
    """
    tool_name = request.get("name")
    arguments = request.get("arguments", {})
    
    if not tool_name:
        raise HTTPException(status_code=400, detail="Tool name is required")
    
    try:
        if tool_name == "scrape_website":
            url = arguments.get("url")
            if not url:
                raise HTTPException(status_code=400, detail="URL is required for scrape_website tool")
            
            # Use existing scraping logic
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text(separator='\n', strip=True)
            database.add_scraped_data(url=url, content=page_text)
            
            return {
                "tool": tool_name,
                "result": f"Successfully scraped and stored content from {url}",
                "content_preview": page_text[:500] + "..." if len(page_text) > 500 else page_text
            }
            
        elif tool_name == "query_agent":
            url = arguments.get("url")
            prompt = arguments.get("prompt")
            
            if not url or not prompt:
                raise HTTPException(status_code=400, detail="Both URL and prompt are required for query_agent tool")
            
            # Check if content exists in memory, scrape if needed
            content = database.get_content_by_url(url)
            if content is None:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                content = soup.get_text(separator='\n', strip=True)
                database.add_scraped_data(url=url, content=content)
            
            # Query the LLM
            ai_response = llm_service.query_llm(context=content, prompt=prompt)
            
            return {
                "tool": tool_name,
                "result": ai_response,
                "url": url,
                "prompt": prompt
            }
            
        elif tool_name == "get_stored_data":
            stored_data = database.get_all_scraped_data()
            return {
                "tool": tool_name,
                "result": stored_data,
                "count": len(stored_data)
            }
            
        elif tool_name == "search_content":
            query = arguments.get("query")
            if not query:
                raise HTTPException(status_code=400, detail="Search query is required for search_content tool")
            
            # Simple search implementation
            stored_data = database.get_all_scraped_data()
            results = []
            
            for item in stored_data:
                content = database.get_content_by_url(item['url'])
                if content and query.lower() in content.lower():
                    results.append({
                        'url': item['url'],
                        'scraped_at': item['scraped_at'],
                        'snippet': content[:200] + "..." if len(content) > 200 else content
                    })
            
            return {
                "tool": tool_name,
                "result": results,
                "query": query,
                "matches_found": len(results)
            }
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Tool execution error: {str(e)}")

# ====== Application Management ======

def run_fastapi_server():
    """Run the FastAPI server"""
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    # Check if running as MCP server or FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
        logger.info("Starting in MCP mode...")
        # For future MCP stdio integration if needed
        print("MCP mode not yet implemented via stdio. Use FastAPI endpoints at /mcp/")
    else:
        logger.info("Starting FastAPI server...")
        run_fastapi_server()