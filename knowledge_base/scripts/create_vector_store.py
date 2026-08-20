from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "knowledge_base" / "raw"

VECTOR_DIR = BASE_DIR / "knowledge_base" / "vector_store"

# ==========================================
# Load PDFs
# ==========================================

documents = []

for pdf in RAW_DIR.rglob("*.pdf"):

    print(f"Loading {pdf.name}")

    loader = PyPDFLoader(str(pdf))

    documents.extend(loader.load())

print(f"\nLoaded Pages : {len(documents)}")

# ==========================================
# Split Documents
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Original Chunks : {len(chunks)}")

# ==========================================
# Clean Chunks
# ==========================================

REMOVE_IF_CONTAINS = [

    "table of contents",

    "contents",

    "references",

    "acknowledgements",

    "copyright",

    "isbn",

    "index"

]

clean_chunks = []

for chunk in chunks:

    text = chunk.page_content.lower()

    if any(word in text for word in REMOVE_IF_CONTAINS):

        continue

    clean_chunks.append(chunk)

print(f"Clean Chunks : {len(clean_chunks)}")

# ==========================================
# MiniLM Embeddings
# ==========================================

print("\nLoading MiniLM Model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating FAISS Vector Store...")

# ==========================================
# Create FAISS
# ==========================================

vector_store = FAISS.from_documents(
    clean_chunks,
    embeddings
)

# ==========================================
# Save
# ==========================================

VECTOR_DIR.mkdir(exist_ok=True)

vector_store.save_local(str(VECTOR_DIR))

print("\n====================================")
print("FAISS Index Created Successfully")
print(f"Saved to : {VECTOR_DIR}")
print("====================================")