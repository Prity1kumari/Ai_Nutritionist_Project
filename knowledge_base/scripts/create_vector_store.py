import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

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
    chunk_size=2500,
    chunk_overlap=250
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
# Google Generative AI Embeddings
# ==========================================

print("\nLoading Google Generative AI Embeddings...")

api_key = os.getenv("GEMINI_EMBEDDING_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GEMINI_EMBEDDING_API_KEY, GEMINI_API_KEY, or GOOGLE_API_KEY not found.")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=api_key
)

# ==========================================
# Create FAISS
# ==========================================

print("Creating FAISS Vector Store in batches to avoid rate limits...")
import time

batch_size = 50
vector_store = None

for i in range(0, len(clean_chunks), batch_size):
    batch = clean_chunks[i : i + batch_size]
    print(f"Embedding batch {i // batch_size + 1}/{(len(clean_chunks) - 1) // batch_size + 1} ({len(batch)} chunks)...")
    
    retries = 5
    delay = 10
    for attempt in range(retries):
        try:
            if vector_store is None:
                vector_store = FAISS.from_documents(batch, embeddings)
            else:
                vector_store.add_documents(batch)
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                print(f"Rate limit hit. Retrying in {delay} seconds (Attempt {attempt+1}/{retries})...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e
    else:
        raise RuntimeError("Failed to embed documents due to persistent rate limits.")
    
    time.sleep(2)

# ==========================================
# Save
# ==========================================

VECTOR_DIR.mkdir(exist_ok=True)

vector_store.save_local(str(VECTOR_DIR))

print("\n====================================")
print("FAISS Index Created Successfully")
print(f"Saved to : {VECTOR_DIR}")
print("====================================")