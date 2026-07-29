import pickle
import numpy as np

from app.core.config import MODEL_PATH
from app.core.logger import logger

# Load model once when the application starts
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise


def predict_health(data):
    """
    Predict the health score of a food item.

    Returns:
        dict: {
            "health_score": int,
            "confidence": float
        }
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

    prediction = model.predict(features)[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(np.max(model.predict_proba(features)))

    return {
        "health_score": int(prediction),
        "confidence": confidence
    }