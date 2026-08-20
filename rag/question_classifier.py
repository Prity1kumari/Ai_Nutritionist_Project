from rag.llm import llm


def classify_question(question: str):

    prompt = f"""
Classify this question.

Return ONLY one word:

FOOD
GENERAL

Question:
{question}
"""

    response = llm.generate_content(prompt)

    return response.text.strip().upper()