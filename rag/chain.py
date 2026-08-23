from pathlib import Path

from rag.question_classifier import classify_question

from knowledge_base.service import get_knowledge
from knowledge_base.retriever import get_retriever

from rag.context_builder import format_ingredient_context
from rag.prompt import build_prompt
from rag.llm import llm
from rag.utils import format_context


def ask_nutritionist(question: str):

    # ==========================
    # Question Classification
    # ==========================

    question_type = classify_question(question)

    print("QUESTION TYPE:", question_type)

    # ==========================
    # General Chat
    # ==========================

    if question_type == "GENERAL":

        response = llm.generate_content(question)

        return {
            "answer": response.text.strip(),
            "sources": []
        }

    # ==========================
    # Ingredient Knowledge
    # ==========================

    ingredient_data = get_knowledge(question)

    ingredient_context = format_ingredient_context(
        ingredient_data
    )

    # ==========================
    # Retriever
    # ==========================

    retriever = get_retriever()

    docs = retriever.invoke(question)

    pdf_context = format_context(docs)

    # ==========================
    # Context
    # ==========================

    context = f"""
========== INGREDIENT INFORMATION ==========

{ingredient_context}

========== DOCUMENT INFORMATION ==========

{pdf_context}
"""

    # ==========================
    # Prompt
    # ==========================

    prompt = build_prompt(
        question,
        context
    )

    print("\n========== PROMPT ==========\n")
    print(prompt[:5000])
    print("\n============================\n")

    # ==========================
    # LLM Response
    # ==========================

    response = llm.generate_content(prompt)

    answer = response.text.strip()

    # ==========================
    # Fallback
    # ==========================

    if (
        not answer
        or "I don't have enough information" in answer
    ):
        print("Using Gemini fallback...")

        response = llm.generate_content(question)

        answer = response.text.strip()

    # ==========================
    # Sources
    # ==========================

    sources = []

    if isinstance(ingredient_data, dict):

        ingredient_name = ingredient_data.get(
            "ingredient",
            "Unknown Ingredient"
        )

        sources.append({
            "type": "ingredient_knowledge",
            "source": f"{ingredient_name}.json"
        })

    for doc in docs:

        source_path = doc.metadata.get("source")

        source = {
            "type": "document",
            "source": (
                Path(source_path).name
                if source_path
                else "Unknown"
            ),
            "page": doc.metadata.get("page")
        }

        if source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }