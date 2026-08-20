import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ALIAS_FILE = BASE_DIR / "aliases" / "aliases.json"

with open(ALIAS_FILE, "r", encoding="utf-8") as f:
    ALIASES = json.load(f)


def extract_ingredient(question: str):

    if not question:
        return None

    question = question.lower().strip()

    # Only return an ingredient if it is explicitly
    # present in the known aliases list.

    for alias, ingredient in sorted(
        ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):

        alias = alias.lower().strip()

        if alias and alias in question:
            return ingredient

    # Absolutely do NOT return the question itself.
    return None