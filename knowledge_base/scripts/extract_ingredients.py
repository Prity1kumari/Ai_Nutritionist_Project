from pathlib import Path
import pandas as pd
from tqdm import tqdm
import re

# ============================================
# DATASET PATH
# ============================================

DATASET_PATH = Path(
    r"C:\Users\prity\OneDrive\Desktop\Ai_Nutritionist_Project\dataset\raw\en.openfoodfacts.org.products.csv"
)

# ============================================
# OUTPUT
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_PATH = BASE_DIR / "processed" / "ingredients.csv"

CHUNK_SIZE = 50000

# ============================================
# CLEAN INGREDIENT
# ============================================

def clean_ingredient(text):

    text = text.lower().strip()

    # remove percentages
    text = re.sub(r"\d+(\.\d+)?%", "", text)

    # remove brackets
    text = re.sub(r"\(.*?\)", "", text)

    # remove unwanted symbols
    text = re.sub(r"[^a-zA-Z0-9\s\-]", "", text)

    text = text.strip()

    return text


# ============================================
# MAIN
# ============================================

print("=" * 60)
print("Extracting Ingredients")
print("=" * 60)

ingredients = set()

reader = pd.read_csv(
    DATASET_PATH,
    sep="\t",
    usecols=["ingredients_text"],
    chunksize=CHUNK_SIZE,
    low_memory=False
)

for chunk in tqdm(reader):

    chunk = chunk.dropna()

    for ingredient_text in chunk["ingredients_text"]:

        ingredient_list = str(ingredient_text).split(",")

        for ingredient in ingredient_list:

            ingredient = clean_ingredient(ingredient)

            if len(ingredient) >= 2:

                ingredients.add(ingredient)

print("\nSaving...")

ingredients = sorted(ingredients)

ingredients_df = pd.DataFrame(
    {"ingredient": ingredients}
)

ingredients_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(f"\nTotal Unique Ingredients : {len(ingredients)}")
print(f"Saved at : {OUTPUT_PATH}")

print("=" * 60)
print("Completed Successfully")
print("=" * 60)