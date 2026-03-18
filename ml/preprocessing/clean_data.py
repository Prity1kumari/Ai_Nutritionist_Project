<<<<<<< HEAD
import numpy as np
import pandas as pd
import re

def clean_data(df):

    # ===============================
    # 1. STANDARDIZE COLUMN NAMES
    # ===============================
    df.columns = df.columns.str.strip().str.lower()

    # Fix common column mismatch
    if "proteins_100g" in df.columns:
        df.rename(columns={"proteins_100g": "protein_100g"}, inplace=True)

    # ===============================
    # 2. REMOVE DUPLICATES
    # ===============================
    df = df.drop_duplicates()

    # ===============================
    # 3. HANDLE MISSING VALUES SMARTLY
    # ===============================
    # Drop rows where target is missing
    df = df.dropna(subset=["nutrition-score-fr_100g"])

    # Fill numeric columns with median
    numeric_cols = [
        "energy_100g", "fat_100g", "saturated-fat_100g",
        "carbohydrates_100g", "sugars_100g",
        "fiber_100g", "protein_100g", "salt_100g"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Fill text column
    if "ingredients_text" in df.columns:
        df["ingredients_text"] = df["ingredients_text"].fillna("unknown")

    # ===============================
    # 4. REMOVE INVALID VALUES
    # ===============================
    # Remove negative values
    for col in numeric_cols:
        if col in df.columns:
            df = df[df[col] >= 0]

    # ===============================
    # 5. REMOVE OUTLIERS (CLIPPING)
    # ===============================
    def clip_outliers(series):
        q1 = series.quantile(0.01)
        q99 = series.quantile(0.99)
        return series.clip(q1, q99)

    for col in numeric_cols:
        if col in df.columns:
            df[col] = clip_outliers(df[col])

    # ===============================
    # 6. FEATURE VALIDATION (REAL-WORLD)
    # ===============================
    # Remove unrealistic food entries
    df = df[df["energy_100g"] > 0]

    # ===============================
    # 7. CLEAN INGREDIENT TEXT
    # ===============================
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9, ]', ' ', text)   # remove special chars
        text = re.sub(r'\s+', ' ', text)              # remove extra spaces
        return text.strip()

    if "ingredients_text" in df.columns:
        df["ingredients_text"] = df["ingredients_text"].apply(clean_text)

    # ===============================
    # 8. REMOVE VERY SHORT TEXT ROWS
    # ===============================
    if "ingredients_text" in df.columns:
        df = df[df["ingredients_text"].str.len() > 5]

    # ===============================
    # 9. RESET INDEX
    # ===============================
    df = df.reset_index(drop=True)

    return df
print("Data cleaning function is ready.")
=======

>>>>>>> 61cdeceb0c5b136049d30400cc7322a4b19be4eb
