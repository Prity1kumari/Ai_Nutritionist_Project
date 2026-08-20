from fastapi import APIRouter, HTTPException

from app.schemas.request import FoodInput
from app.services.ml_service import predict_health
from app.services.ingredient_service import (
    analyze_ingredients_llm,
    generate_food_summary
)
from app.core.logger import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["AI Nutritionist"]
)


@router.post(
    "/predict",
    summary="Predict Food Health Score",
    description="Predicts the health grade of a food product and analyzes harmful ingredients."
)
def predict(data: FoodInput):

    try:

        # -------------------------
        # ML Prediction
        # -------------------------
        prediction = predict_health(data)

        # -------------------------
        # Gemini Ingredient Analysis
        # -------------------------
        ingredient_analysis = analyze_ingredients_llm(
            data.ingredients
        )

        # -------------------------
        # AI Summary
        # -------------------------
        summary = generate_food_summary(
            prediction["grade"],
            ingredient_analysis
        )

        return {

            "success": True,

            "message": "Prediction completed successfully.",

            "data": {

                "health_grade": prediction["grade"],

                "health_description": prediction["description"],

                "confidence": prediction["confidence"],

                "ingredient_analysis": ingredient_analysis,

                "summary": summary

            }

        }

    except Exception as e:

        logger.error(f"Prediction API Error : {e}")

        raise HTTPException(
            status_code=500,
            detail="Prediction Failed."
        )


@router.get("/health")
def health():

    return {

        "status": "Healthy",

        "service": "AI Nutritionist API",

        "version": "1.0.0"

    }


from app.services.ingredient_service import analyze_ingredients_llm

@router.get("/gemini-test")
def gemini_test():

    result = analyze_ingredients_llm(
        "Sugar, Palm Oil, Sodium Nitrate"
    )

    return result