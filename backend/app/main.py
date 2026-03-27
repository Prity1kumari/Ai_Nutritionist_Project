from fastapi import FastAPI
from app.routes.predict import router

app = FastAPI(title="AI Nutritionist API")

app.include_router(router)