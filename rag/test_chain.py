import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rag.chain import ask_nutritionist

print("=" * 60)
print("AI Nutritionist")
print("=" * 60)

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    result = ask_nutritionist(question)

    print("\n" + "=" * 60)
    print("Answer")
    print("=" * 60)

    print(result["answer"])

    print("\nSources")

    for source in result["sources"]:
        print(
            f"- {Path(source['source']).name} (Page {source['page']})"
        )