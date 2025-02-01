# 🤖 AI Agent Telegram Bot  

An AI-powered **Telegram bot** using **Gemini AI**, **MongoDB**, and **Flask**, featuring **web search**, **sentiment analysis**, **file analysis**, and a **user analytics dashboard**.

---

## 🚀 Features  

✅ **AI-powered chat** (Gemini API for intelligent responses)  
✅ **User registration** (MongoDB stores user details)  
✅ **Sentiment analysis** (TextBlob evaluates emotions in messages)  
✅ **Web search** (Fetches top results from DuckDuckGo API)  
✅ **File analysis** (Gemini AI describes uploaded documents)  
✅ **Analytics dashboard** (Flask-based user & message tracking)  

## 📌 Tech Stack  

| **Component**     | **Technology Used**                         |
|------------------|-------------------------------------|
| **Backend**      | Python, Flask, MongoDB, Telegram Bot API |
| **AI Model**     | Google Gemini AI                         |
| **Database**     | MongoDB (via PyMongo)                   |
| **NLP**          | TextBlob (Sentiment Analysis)           |
| **Web Scraping** | DuckDuckGo API (for web search)         |
| **Deployment**   | Local / Cloud hosting                   |


## 🛠️ Setup Guide  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/vharishcse/ai-agent-telegram-bot.git
cd ai-agent-telegram-bot
```

### **2️⃣ Create a Virtual Environment**  
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### **3️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **4️⃣ Create a `.env` File**  
Create a `.env` file in the project root directory and add your credentials:  

```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MONGO_URI=your_mongodb_uri
GEMINI_API_KEY=your_gemini_api_key
```

### **5️⃣ Run the Bot**  
```sh
python bot.py
```

### **6️⃣ Run the Dashboard**  
```sh
python dashboard.py
```

---

## 📜 Available Commands  

```plaintext
/start - Register with the bot
/chat <message> - Chat with the AI
/upload - Upload and analyze a document
/websearch <query> - Perform a web search
/sentiment <text> - Analyze sentiment
/help - Display available commands
```

---

## 🖥️ **Analytics Dashboard**  

The Flask dashboard provides real-time insights into:  

📊 **Total Registered Users**  
💬 **Total Messages Processed**  

To access the dashboard, run:  
```sh
python dashboard.py
```
Then, open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🛠 Dependencies  
Updated `requirements.txt`:
```
Flask==3.1.0
google-ai-generativelanguage==0.6.15
google-api-core==2.24.1
google-api-python-client==2.160.0
google-auth==2.38.0
google-generativeai==0.8.4
googleapis-common-protos==1.66.0
grpcio==1.70.0
grpcio-status==1.70.0
pymongo==4.11
requests==2.32.3
textblob==0.19.0
python-dotenv==1.0.1
python-telegram-bot==21.10
nltk==3.9.1
Werkzeug==3.1.3
Jinja2==3.1.5
```

## 🔄 Updating and Pushing to GitHub  

After making changes, use the following commands to push updates:
```sh
git add .
git commit -m "Updated README and dependencies"
git push origin main
```

---

## 📌 **Contributing**  

👨‍💻 Contributions are welcome! If you'd like to improve the bot, feel free to fork this repo and submit a pull request.  

---

## 👨‍💻 **Author**  

**Harish Yadav** 🚀  
🔗 [LinkedIn](https://www.linkedin.com/in/v-harish-yadav-b2bb52241)  

---

## 📜 **License**  
This project is **open-source** and available under the **MIT License**.

