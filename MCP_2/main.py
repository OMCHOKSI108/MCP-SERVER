from fastapi import FastAPI, HTTPException
from crawl4ai import Crawl4AI
import database  # Import our new database module

# Create a FastAPI app instance
app = FastAPI()

@app.on_event("startup")
def on_startup():
    """This function runs when the FastAPI application starts."""
    database.init_db()

@app.get("/")
def read_root():
    """ A default endpoint to welcome users to your API. """
    return {"message": "Welcome to the Crawl4AI Web Scraping Agent API"}

@app.post("/scrape/")
async def scrape_website(url: str):
    """
    Scrapes a URL with Crawl4AI and saves the clean Markdown to the database.
    """
    try:
        crawler = Crawl4AI()
        result = crawler.run(url=url)

        if not result or not result.documents:
            raise HTTPException(status_code=404, detail="Could not extract content from the URL.")

        markdown_content = result.documents[0].page_content

        # --- NEW: Save the result to the database ---
        database.add_scraped_data(url=url, content=markdown_content)
        # -------------------------------------------

        return {
            "url": url,
            "message": "Content successfully scraped and stored.",
            "scraped_content_markdown": markdown_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/data/")
async def view_stored_data():
    """
    A new endpoint to view all the data stored in the agent's memory.
    """
    stored_data = database.get_all_scraped_data()
    return {"agent_memory": stored_data}