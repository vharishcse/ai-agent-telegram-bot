from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["your_database"]

@app.route("/")
def index():
    user_count = db.users.count_documents({})
    message_count = db.chat_history.count_documents({})
    return f"<h1>Bot Analytics</h1><p>Users: {user_count}</p><p>Messages: {message_count}</p>"

if __name__ == "__main__":
    app.run(debug=True)