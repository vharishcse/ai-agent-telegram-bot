import os
from serpapi import GoogleSearch
import logging
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
from textblob import TextBlob

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure API key is configured
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini AI model
model = genai.GenerativeModel("gemini-pro")

# Connect to MongoDB
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["your_database"]
users_collection = db["users"]

# Setup logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Initialize the bot
app = Application.builder().token(TOKEN).build()

# User Registration
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id

    # Check if user exists
    if not users_collection.find_one({"chat_id": chat_id}):
        users_collection.insert_one({"chat_id": chat_id, "first_name": user.first_name, "username": user.username})
        await update.message.reply_text(
            "Welcome! Please share your phone number.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Share Contact", request_contact=True)]], one_time_keyboard=True
            ),
        )
    else:
        await update.message.reply_text("You're already registered!")

async def save_contact(update: Update, context: CallbackContext) -> None:
    contact = update.message.contact
    chat_id = update.message.chat_id
    if contact:
        users_collection.update_one({"chat_id": chat_id}, {"$set": {"phone_number": contact.phone_number}})
        await update.message.reply_text("Phone number saved successfully!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        # Generate response from Gemini AI
        response = model.generate_content(user_message)
        reply = response.text  
    except Exception as e:
        reply = "Error processing your request. Please try again later."
        logging.error(f"Gemini AI Error: {e}")

    # Save chat to MongoDB
    db.chat_history.insert_one({"chat_id": update.message.chat_id, "user_message": user_message, "bot_response": reply})

    await update.message.reply_text(reply)

# File Handling
import os

async def handle_document(update: Update, context: CallbackContext):
    file_id = update.message.document.file_id
    file = await context.bot.get_file(file_id)

    # Ensure the "downloads" directory exists
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    # Define file path
    file_path = os.path.join(download_dir, update.message.document.file_name)

    # Download the file
    await file.download_to_drive(file_path)

    # Send confirmation message
    await update.message.reply_text(f"✅ File '{update.message.document.file_name}' uploaded successfully!")

    # Optional: Analyze only PDF or Word files
    if file_path.endswith(".pdf") or file_path.endswith(".docx"):
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()

            # Send file to Gemini AI for analysis
            response = model.generate_content(["Describe this file:", file_content])
            description = response.text

            # Save file metadata in MongoDB
            db.file_metadata.insert_one({
                "chat_id": update.message.chat_id,
                "filename": update.message.document.file_name,
                "description": description
            })

            await update.message.reply_text(f"📄 **File Analysis:**\n{description}")

        except Exception as e:
            await update.message.reply_text("⚠️ Error analyzing the file.")
            logging.error(f"File Processing Error: {e}")

# Web Search
async def web_search(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide a search query. Example: /websearch AI trends")
        return

    query = " ".join(context.args)
    api_key = os.getenv("SERPAPI_KEY")  # Store API key in .env file

    params = {
        "q": query,
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        search_results = results.get("organic_results", [])

        if not search_results:
            await update.message.reply_text("No results found. Try a different query.")
            return

        # Extract top 3 search results
        top_results = "\n".join(
            [f"- [{r['title']}]({r['link']})" for r in search_results[:3]]
        )

        await update.message.reply_text(f"🔍 **Top Search Results:**\n{top_results}", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error during web search: {e}")
        await update.message.reply_text("An error occurred while performing the search. Please try again later.")

# Sentiment Analysis
async def analyze_sentiment(update: Update, context: CallbackContext):
    if update.message.text.startswith("/sentiment"):
        text = update.message.text[len("/sentiment"):].strip()

        if not text:
            await update.message.reply_text("Please provide text after '/sentiment' for analysis.")
            return

        sentiment = TextBlob(text).sentiment.polarity

        if sentiment > 0:
            sentiment_response = "🙂 Positive"
        elif sentiment < 0:
            sentiment_response = "😞 Negative"
        else:
            sentiment_response = "😐 Neutral"

        await update.message.reply_text(f"Sentiment Analysis: {sentiment_response}")

#handle document
async def upload_instruction(update: Update, context: CallbackContext):
    await update.message.reply_text("Please send a document to analyze.")

#handle chat Command
async def chat(update: Update, context: CallbackContext):
    user_message = " ".join(context.args)  # Get the text after "/chat"

    if not user_message:
        await update.message.reply_text("Please enter a message after /chat.")
        return

    try:
        # Generate response from Gemini AI
        prompt = f"You are a friendly AI assistant. Respond in a casual and helpful tone. User: {user_message}"
        response = model.generate_content(prompt)
        reply = response.text  # Extract AI response
    except Exception as e:
        reply = "Error processing your request. Please try again later."
        logging.error(f"Gemini AI Error: {e}")

    await update.message.reply_text(reply)

#help command
async def help_command(update: Update, context: CallbackContext):
    help_text = """🛠 **Available Commands:**
    
    /start - Register with the bot  
    /chat <message> - Chat with the AI  
    /upload - Upload and analyze a document  
    /websearch <query> - Perform a web search  
    /sentiment <text> - Analyze sentiment  

    🔹 *Try sending a message or uploading a file!*"""
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Handlers
app.add_handler(CommandHandler("chat", chat))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, save_contact))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("upload", upload_instruction))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(CommandHandler("websearch", web_search))
app.add_handler(CommandHandler("sentiment", analyze_sentiment))
app.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    print("Starting the bot...")
    app.run_polling()
