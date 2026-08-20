import json
from pathlib import Path

from knowledge_base.enricher import enrich_ingredient
from knowledge_base.extractor import extract_ingredient


BASE_DIR = Path(__file__).resolve().parent

CACHE_DIR = BASE_DIR / "ingredient_cache"
CACHE_DIR.mkdir(exist_ok=True)


def ingredient_filename(name: str):
    return name.lower().replace(" ", "_") + ".json"


def ingredient_exists(name: str):
    return (CACHE_DIR / ingredient_filename(name)).exists()


def load_ingredient(name: str):

    path = CACHE_DIR / ingredient_filename(name)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ingredient(name: str, data: dict):

    path = CACHE_DIR / ingredient_filename(name)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_ingredient_data(question: str):

    ingredient = extract_ingredient(question)

    # No known ingredient
    if ingredient is None:
        print("ℹ️ No known ingredient detected")
        return None

    # Cache hit
    if ingredient_exists(ingredient):

        print(f"✅ Cache Hit: {ingredient}")

        return load_ingredient(ingredient)

    # Cache miss
    print(f"⚡ Cache Miss: {ingredient}")

    data = enrich_ingredient(ingredient)

    save_ingredient(ingredient, data)

    return data