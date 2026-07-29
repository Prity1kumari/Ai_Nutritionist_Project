import google.generativeai as genai
import json

from app.core.config import GOOGLE_API_KEY, GEMINI_MODEL

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize model once
model = genai.GenerativeModel(GEMINI_MODEL)


def analyze_ingredients_llm(ingredients):
    prompt = f"""
    You are a nutrition expert.

    Analyze the following ingredients:
    {ingredients}

    Identify harmful or risky ingredients and explain briefly.

    Return ONLY valid JSON in this format:

    [
      {{
        "ingredient": "name",
        "risk": "short explanation"
      }}
    ]
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by Gemini",
            "raw_output": text
        }