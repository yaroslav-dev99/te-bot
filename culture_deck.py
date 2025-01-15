import openai
import requests
from bs4 import BeautifulSoup
from config import OPENAI_API_KEY

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Function to fetch the Culture Deck content from a URL
def fetch_culture_deck_from_url(url):
    try:
        # Send a GET request to fetch the Culture Deck content
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text  # Return raw content (modify for parsing if needed)
        else:
            return "Error: Unable to fetch the Culture Deck from the provided link."
    except Exception as e:
        return f"Error: {str(e)}"

# Parse the HTML with BeautifulSoup
def extract_text_from_html(soup):
    # Get the full text content (you can adjust this based on structure)
    span_tags = soup.find_all('span', class_='kr-span')
    text_content = ""
    for span in span_tags:
        text_content = text_content + "\n\n" + span.text
            # text_content = soup.get_text(separator="\n", strip=True)
    return text_content

def fetch_culture_text(culture_deck_url):
    # Fetch the HTML content
    soup = BeautifulSoup(fetch_culture_deck_from_url(culture_deck_url), "html.parser")
    # Extract the text
    culture_text = extract_text_from_html(soup)
    return culture_text

# Function to test the candidate's understanding
def test_understanding(question):
    # Return a simple test question to follow up
    # This can be dynamic based on the question or a preset question from the Culture Deck
    return "Why is a Wartime CEO necessary in a company like Latoken?"

# culture_deck_url = "https://coda.io/@latoken/latoken-talent/what-and-why-we-do-107"
# culture_content = fetch_culture_text(culture_deck_url)
