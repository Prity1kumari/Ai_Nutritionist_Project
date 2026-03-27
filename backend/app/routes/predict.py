from fastapi import APIRouter
from app.schemas.request import FoodInput
from app.services.ml_service import predict_health
from app.services.ingredient_service import analyze_ingredients_llm



router = APIRouter()



@router.post("/predict")
def predict(data: FoodInput):

    result = predict_health(data)
    risks= analyze_ingredients_llm(data.ingredients)

    return {
        "health_score": result,
        "ingredient_analysis": risks
    }
@router.get("/test")
def test():
    return {
        "Test message": "How are you"
    }
