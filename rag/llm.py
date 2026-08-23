import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# ======================================
# Load .env
# ======================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found.")

# Change this whenever Google releases a new model
GEMINI_MODEL = "models/gemini-3.6-flash"

genai.configure(api_key=GOOGLE_API_KEY)

llm = genai.GenerativeModel(GEMINI_MODEL)