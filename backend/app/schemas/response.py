from pydantic import BaseModel
from typing import List


class IngredientRisk(BaseModel):

    ingredient: str
    risk: str


class PredictionResponse(BaseModel):

    health_grade: str

    health_description: str

    confidence: float | None

    ingredient_analysis: List[IngredientRisk]