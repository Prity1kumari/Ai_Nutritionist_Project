from pydantic import BaseModel

class FoodInput(BaseModel):
    energy: float
    fat: float
    saturated_fat: float
    carbs: float
    sugar: float
    fiber: float
    protein: float
    salt: float