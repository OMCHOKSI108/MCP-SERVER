from fastapi import FastAPI
import requests
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

# Create a FastAPI app instance
app = FastAPI()

@app.get("/")
def read_root():
    """ A default endpoint to welcome users to your API. """
    return {"message": "Welcome to the Web Scraping Agent API"}

@app.post("/scrape/")
def scrape_website(url: str):
    """
    This endpoint takes a URL, scrapes its content,
    and returns the extracted text.
    
    """
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the text from the page
        page_text = soup.get_text(separator='\n', strip=True)

        return {"url": url, "content": page_text}

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve the URL: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}