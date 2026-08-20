from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predict import router
from app.api.chat import router as chat_router
from app.core.config import API_TITLE, API_VERSION

app = FastAPI(
    title="AI Nutritionist API",
    version="1.0.0",
    description="AI-powered Nutrition Analysis API using Machine Learning and Gemini AI."
)

app.include_router(chat_router)

# ==========================
# CORS Configuration
# ==========================

origins = [
    "http://localhost:3000",   # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Register Routes
# ==========================

app.include_router(router)

# ==========================
# Root Endpoint
# ==========================

@app.get("/")
def root():
    return {
        "message": "AI Nutritionist API is Running 🚀",
        "version": API_VERSION
    }