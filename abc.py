import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("GEMINI_API_KEY"))  # Check if it's loaded correctly
