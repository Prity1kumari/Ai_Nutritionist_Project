import json
import google.generativeai as genai

from app.core.config import GOOGLE_API_KEY, GEMINI_MODEL
from app.core.logger import logger

# ==========================================
# Configure Gemini
# ==========================================

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


# ==========================================
# Prompt Builder
# ==========================================

def build_prompt(ingredients: str) -> str:

    return f"""
You are an experienced clinical nutritionist.

Analyze ONLY the ingredients listed below.

Ingredients:
{ingredients}

Instructions:
1. Identify ingredients that may pose health risks.
2. Ignore ingredients that are generally considered safe.
3. Explain each risk in simple language.
4. Keep each explanation under 25 words.
5. If no harmful ingredients exist, return an empty list.

Return ONLY valid JSON.

Example:

[
    {{
        "ingredient": "Sugar",
        "risk": "Excessive intake may increase the risk of obesity and diabetes."
    }},
    {{
        "ingredient": "Palm Oil",
        "risk": "High in saturated fat which may increase LDL cholesterol."
    }}
]
"""


# ==========================================
# Clean Gemini Output
# ==========================================

def clean_json(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return text


# ==========================================
# Ingredient Analysis
# ==========================================

def analyze_ingredients_llm(ingredients: str):

    try:

        logger.info("Sending ingredient list to Gemini...")

        prompt = build_prompt(ingredients)

        response = model.generate_content(prompt)

        text = clean_json(response.text)

        risks = json.loads(text)

        logger.info("Ingredient analysis completed successfully.")

        return risks

    except json.JSONDecodeError as e:

        logger.error(f"JSON Parsing Error: {e}")

        return [
            {
                "ingredient": "Unknown",
                "risk": "Unable to parse Gemini response."
            }
        ]

    except Exception as e:

        logger.error(f"Gemini Error: {e}")

        return [
            {
                "ingredient": "System",
                "risk": "Ingredient analysis temporarily unavailable."
            }
        ]


# ==========================================
# AI Food Summary
# ==========================================

def generate_food_summary(grade: str, risks: list):

    prompt = f"""
You are a certified nutrition expert.

Health Grade:
{grade}

Ingredient Risks:
{json.dumps(risks, indent=2)}

Write a short summary for a normal person.

Rules:
- Maximum 60 words.
- Use simple English.
- Mention whether the food is healthy or unhealthy.
- Mention if it should be consumed regularly or occasionally.
"""

    try:

        logger.info("Generating AI summary...")

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:

        logger.error(f"Summary Generation Error: {e}")

        return "Summary unavailable."