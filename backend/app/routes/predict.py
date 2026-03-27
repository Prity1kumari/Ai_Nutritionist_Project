from fastapi import APIRouter
from app.schemas.request import FoodInput
from app.services.ml_service import predict_health

router = APIRouter()

@router.post("/predict")
def predict(data: FoodInput):

    result = predict_health(data)

    return {
        "health_score": result
    }
@router.get("/test")
def test():
    return {
        "Test message": "How are you"
    }