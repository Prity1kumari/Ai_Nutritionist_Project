from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

# ===========================================
# KNOWLEDGE BASE ROOT
# ===========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "raw"

# ===========================================
# LOAD ALL PDFs
# ===========================================

documents = []

for pdf in RAW_DIR.rglob("*.pdf"):

    print(f"Loading {pdf.name}")

    loader = PyPDFLoader(str(pdf))

    docs = loader.load()

    documents.extend(docs)

print("\n===================================")
print(f"Total Pages Loaded : {len(documents)}")
print("===================================\n")

# Print first page
print(documents[0].page_content[:1000])

print("\nMetadata")

print(documents[0].metadata)