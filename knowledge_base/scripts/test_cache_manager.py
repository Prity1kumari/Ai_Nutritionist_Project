import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_base.cache_manager import get_ingredient_data

while True:

    question = input("\nQuestion (type 'exit' to quit): ").strip()

    if question.lower() == "exit":
        break

    result = get_ingredient_data(question)

    print("\nResult:\n")
    print(result)