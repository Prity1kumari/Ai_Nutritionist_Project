from pathlib import Path
from functools import lru_cache

import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"
load_dotenv(BASE_DIR.parent / ".env")


@lru_cache(maxsize=1)
def get_retriever():

    api_key = os.getenv("GEMINI_EMBEDDING_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_EMBEDDING_API_KEY, GEMINI_API_KEY, or GOOGLE_API_KEY not found.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=api_key
    )

    vector_store = FAISS.load_local(
        str(VECTOR_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )