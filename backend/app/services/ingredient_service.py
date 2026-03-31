import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def analyze_ingredients_llm(ingredients):

    prompt = f"""
    You are a nutrition expert.

    Analyze the following ingredients:
    {ingredients}

    Identify harmful or risky ingredients and explain briefly.

    Return ONLY JSON in this format:
    [
      {{
        "ingredient": "name",
        "risk": "short explanation"
      }}
    ]
    """

    response = model.generate_content(prompt)

    text = response.text

    try:
        return json.loads(text)
    except:
        return {"raw_output": text}