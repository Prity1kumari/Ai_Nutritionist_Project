import os
from pathlib import Path
from dotenv import load_dotenv

# ======================================
# Project Root
# ======================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ======================================
# Load Environment Variables
# ======================================

load_dotenv(BASE_DIR / ".env")

# ======================================
# API Configuration
# ======================================

API_TITLE = os.getenv("API_TITLE", "AI Nutritionist API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

# ======================================
# Gemini Configuration
# ======================================

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY or GOOGLE_API_KEY not found. Please add it to the project root .env"
    )

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-3.6-flash")

# ======================================
# ML Model Path
# ======================================

MODEL_PATH = BASE_DIR / "ml" / "models" / "nutrition_model.pkl"