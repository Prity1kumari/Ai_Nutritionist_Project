import json


def format_ingredient_context(data: dict):

    if data is None:
        return ""

    text = f"""
Ingredient:
{data.get("ingredient","")}

Aliases:
{", ".join(data.get("aliases", []))}

Category:
{data.get("category","")}

Description:
{data.get("description","")}

Health Effects:
"""

    for effect in data.get("health_effects", []):
        text += f"\n- {effect}"

    text += "\n\nCommon Foods:\n"

    for food in data.get("common_foods", []):
        text += f"- {food}\n"

    text += "\nSafer Alternatives:\n"

    for alt in data.get("safer_alternatives", []):
        text += f"- {alt}\n"

    return text