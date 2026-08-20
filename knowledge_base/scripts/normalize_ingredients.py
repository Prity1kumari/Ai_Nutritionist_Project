from pathlib import Path
import pandas as pd
import json
import re

# ===========================================
# PATHS
# ===========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "processed" / "ingredients.csv"

OUTPUT_PATH = BASE_DIR / "processed" / "normalized_ingredients.csv"

ALIAS_PATH = BASE_DIR / "config" / "aliases.json"

# ===========================================
# LOAD ALIASES
# ===========================================

with open(ALIAS_PATH, "r", encoding="utf-8") as f:
    aliases = json.load(f)

# ===========================================
# NORMALIZATION
# ===========================================

def normalize(text):

    text = text.lower()

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    if text in aliases:
        text = aliases[text]

    return text

# ===========================================
# LOAD DATA
# ===========================================

df = pd.read_csv(INPUT_PATH)

print("Normalizing ingredients...")

df["normalized"] = df["ingredient"].apply(normalize)

df = df.drop_duplicates(subset=["normalized"])

df.to_csv(OUTPUT_PATH, index=False)

print(f"Total Ingredients : {len(df)}")

print(f"Saved : {OUTPUT_PATH}")