import os
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv(BASE_DIR / ".env")

# -----------------------------
# API Keys
# -----------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# -----------------------------
# ML Model Path
# -----------------------------
MODEL_PATH = BASE_DIR / "ml" / "models" / "nutrition_model.pkl"

# -----------------------------
# API Configuration
# -----------------------------
API_TITLE = "AI Nutritionist API"
API_VERSION = "1.0.0"

# -----------------------------
# Gemini Configuration
# -----------------------------
GEMINI_MODEL = "gemini-1.5-flash"

# -----------------------------
# Logging
# -----------------------------
LOG_LEVEL = "INFO"