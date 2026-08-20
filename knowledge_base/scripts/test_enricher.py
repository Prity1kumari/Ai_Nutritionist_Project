import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.enricher import enrich_ingredient

ingredient = input("Ingredient: ")

data = enrich_ingredient(ingredient)

print()

print(data)