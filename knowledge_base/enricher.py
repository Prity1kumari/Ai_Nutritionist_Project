import json
import re

from rag.llm import llm


def build_prompt(ingredient: str, aliases=None):

    aliases = aliases or []

    alias_text = ", ".join(aliases) if aliases else "None"

    return f"""
You are a food safety and nutrition expert.

Generate information ONLY for this ingredient.

Ingredient:
{ingredient}

Known Aliases:
{alias_text}

Return ONLY valid JSON.

Schema:

{{
    "ingredient": "",
    "aliases": [],
    "category": "",
    "description": "",
    "health_effects": [],
    "common_foods": [],
    "safer_alternatives": []
}}

Rules:

- No markdown
- No explanation
- No extra text
- Only valid JSON
"""


def enrich_ingredient(ingredient: str, aliases=None):

    prompt = build_prompt(ingredient, aliases)

    response = llm.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if Gemini adds it
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    return json.loads(text)