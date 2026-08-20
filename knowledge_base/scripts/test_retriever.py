import sys
from pathlib import Path

# ======================================
# Add Project Root to Python Path
# ======================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# ======================================
# Import Retriever
# ======================================

from knowledge_base.retriever import retriever

# ======================================
# Test
# ======================================

query = input("Ask your question: ")

docs = retriever.invoke(query)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(docs, start=1):
    print("=" * 80)
    print(f"Document {i}")
    print("=" * 80)
    print(doc.page_content)
    print("\nMetadata:")
    print(doc.metadata)
    print()