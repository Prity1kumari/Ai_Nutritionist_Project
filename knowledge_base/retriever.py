from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

VECTOR_DIR = BASE_DIR / "vector_store"

# ==========================================
# Load Embedding Model
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# Load FAISS
# ==========================================

vector_store = FAISS.load_local(
    str(VECTOR_DIR),
    embeddings,
    allow_dangerous_deserialization=True
)

# ==========================================
# Retriever
# ==========================================

retriever = vector_store.as_retriever(

    search_type="similarity",

    search_kwargs={
        "k": 4
    }

)

print("Retriever Ready")