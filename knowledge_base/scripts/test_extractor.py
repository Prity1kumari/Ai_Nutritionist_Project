import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.extractor import extract_ingredient

while True:

    q = input("Question (type 'exit' to quit): ").strip()

    if q.lower() == "exit":
        print("\nExiting Ingredient Extractor...")
        break

    ingredient = extract_ingredient(q)

    print("\nIngredient:\n")
    print(ingredient)