import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from culture_deck import fetch_culture_text, test_understanding
from config import TELEGRAM_API_KEY, OPENAI_API_KEY
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up Telegram bot token
TELEGRAM_API_KEY = TELEGRAM_API_KEY

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am the LATOKEN AI Bot. How can I help you with learning about Latoken and the Hackathon?")

# Help command handler
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("You can ask me anything about Latoken, the Hackathon, or our Culture Deck.")

# Function to split long text into chunks of max 4096 characters
def split_message(text, max_length=4096):
    """Splits a message into multiple parts if it exceeds the maximum allowed length."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Function to strip HTML tags using BeautifulSoup
def strip_html_tags(html_text):
    """Removes HTML tags from the response using BeautifulSoup."""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()

# Handle questions
async def answer_question(update: Update, context: CallbackContext):
    question = update.message.text
    # Culture deck URL (replace with actual URL)
    culture_deck_url = "https://coda.io/@latoken/latoken-talent/what-and-why-we-do-107"
    # culture_deck_url = "https://coda.io/@latoken/latoken-talent/latoken-161"

    # Get the answer from the Culture Deck (assuming this returns HTML content)
    # answer = fetch_answer_from_culture_deck(question, culture_deck_url)
    culture_content = fetch_culture_text(culture_deck_url)
    completion  = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Answer the following question based on the LATOKEN culture:\n\n{culture_content}\n\nQuestion: {question}\n\nPlease answer In English.",
            },
        ],
    )
    # async for chunk in stream:
    #     await update.message.reply_text(chunk.choices[0].delta.content or "", end="")
    await update.message.reply_text(completion.choices[0].message.content)
    # Ask a follow-up test question
    test_question = test_understanding(question)
    await update.message.reply_text(f"Follow-up question: {test_question}")

# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
