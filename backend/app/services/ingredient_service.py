from langchain_google_genai import ChatGoogleGenrativeAI
from langchain_core.prompts import PromptTemplate

import os
import json

from dotenv import load_dotenv

load_dotenv()


llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)


prompt=PromptTemplate(
    input_variables=["ingredients"],
    template= """
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
)

chain = prompt | llm


def analyze_ingredients_llm(ingredients: str):

    response = chain.invoke({"ingredients": ingredients})

    text = response.content.strip()

    # 🔥 clean markdown if Gemini returns ```json
    if "```" in text:
        text = text.split("```")[1]

    try:
        return json.loads(text)
    except:
        return {"raw_output": text}
