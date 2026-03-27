import os
import pickle
import numpy as np
# go 3 levels up → backend/app/services → backend → project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "nutrition_model.pkl")

print("MODEL PATH:", MODEL_PATH)  # debug

model = pickle.load(open(MODEL_PATH, "rb"))

def predict_health(data):
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

    prediction = model.predict(features)

    return int(prediction[0])  # if encoded