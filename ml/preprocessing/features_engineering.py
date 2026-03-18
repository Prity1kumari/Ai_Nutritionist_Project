import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_target(df, mode="multiclass"):

    # ===============================
    # 1. VALIDATION
    # ===============================
    if "nutrition-score-fr_100g" not in df.columns:
        raise ValueError("Target column not found!")

    # ===============================
    # 2. VECTORIZED CONVERSION (FAST)
    # ===============================
    score = df["nutrition-score-fr_100g"]

    conditions = [
        score <= -1,
        (score > -1) & (score <= 2),
        (score > 2) & (score <= 10),
        (score > 10) & (score <= 18),
        score > 18
    ]

    choices = ["A", "B", "C", "D", "E"]

    df["nutriscore_grade"] = np.select(conditions, choices, default="Unknown")

    # ===============================
    # 3. OPTIONAL: BINARY TARGET
    # ===============================
    if mode == "binary":
        df["target"] = df["nutriscore_grade"].apply(
            lambda x: "Healthy" if x in ["A", "B"] else "Unhealthy"
        )

    else:
        df["target"] = df["nutriscore_grade"]

    # ===============================
    # 4. LABEL ENCODING (FOR ML)
    # ===============================
    le = LabelEncoder()
    df["target_encoded"] = le.fit_transform(df["target"])

    # Save mapping (IMPORTANT for inference)
    label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Label Mapping:", label_mapping)

    return df, le

print("feature engineering function is ready")