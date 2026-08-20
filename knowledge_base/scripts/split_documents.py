from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# Load PDFs
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"

documents = []

for pdf in RAW_DIR.rglob("*.pdf"):

    loader = PyPDFLoader(str(pdf))

    documents.extend(loader.load())

print(f"Loaded Pages : {len(documents)}")

# ==========================================
# Split Documents
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Total Chunks : {len(chunks)}")

print("\n============================")
print("First Chunk")
print("============================\n")

print(chunks[0].page_content)

print("\nMetadata\n")

print(chunks[0].metadata)