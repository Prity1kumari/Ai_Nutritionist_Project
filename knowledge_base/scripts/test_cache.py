import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.cache_manager import *

ingredient = input("Ingredient: ")

print()

print("Exists:", ingredient_exists(ingredient))

print()

print(load_ingredient(ingredient))