import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API client with your API key
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except TypeError:
    raise ValueError("GOOGLE_API_KEY is not set in the .env file or is invalid.")

# Initialize the Generative Model
# We use gemini-2.0-flash as it's fast and powerful for this task.
model = genai.GenerativeModel('gemini-2.0-flash')

def query_llm(context: str, prompt: str) -> str:
    """
    Sends the scraped context and a user prompt to the Gemini LLM for a response.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    # Construct the full prompt for the Gemini model
    full_prompt = (
        "You are a helpful assistant. Your job is to answer the question or perform the task "
        "based *only* on the provided webpage content.\n\n"
        f"--- WEBPAGE CONTENT ---\n{context}\n\n"
        f"--- USER REQUEST ---\n{prompt}"
    )

    try:
        # Generate the content using the model
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I was unable to process the request with the AI model."