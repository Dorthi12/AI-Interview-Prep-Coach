from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

print(GEMINI_API_KEY[:5])
