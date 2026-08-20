import pickle
import numpy as np

from app.core.config import MODEL_PATH
from app.core.logger import logger


# ==========================
# Health Grade Mapping
# ==========================

GRADE_MAP = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E"
}

DESCRIPTION_MAP = {
    "A": "Very Healthy",
    "B": "Healthy",
    "C": "Moderately Healthy",
    "D": "Less Healthy",
    "E": "Unhealthy"
}


# ==========================
# Load Model Once
# ==========================

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    logger.info("Nutrition model loaded successfully.")

except Exception as e:
    logger.error(f"Unable to load model: {e}")
    raise


# ==========================
# Prediction Function
# ==========================

def predict_health(data):
    """
    Predict the health score of a food item.
    """

    features = np.array([[
        data.energy,
        data.fat,
        data.saturated_fat,
        data.carbs,
        data.sugar,
        data.fiber,
        data.protein,
        data.salt
    ]])

    logger.info(f"Input Features: {features.tolist()}")

    # Prediction
    prediction = int(model.predict(features)[0])

    # Confidence
    confidence = None

    if hasattr(model, "predict_proba"):
        confidence = round(
            float(np.max(model.predict_proba(features))),
            2
        )

    grade = GRADE_MAP.get(prediction, "Unknown")

    logger.info(
        f"Prediction={prediction}, Grade={grade}, Confidence={confidence}"
    )

    return {
        "score": prediction,
        "grade": grade,
        "description": DESCRIPTION_MAP.get(grade, "Unknown"),
        "confidence": confidence
    }