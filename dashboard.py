from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["your_database"]

@app.route("/")
def index():
    user_count = db.users.count_documents({})
    message_count = db.chat_history.count_documents({})
    return render_template("index.html", user_count=user_count, message_count=message_count)

if __name__ == "__main__":
    app.run(debug=True)
