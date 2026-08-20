import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.service import get_knowledge

while True:

    question = input("\nQuestion (type 'exit' to quit): ").strip()

    if question.lower() == "exit":
        break

    result = get_knowledge(question)

    print("\nKnowledge:\n")

    print(result)