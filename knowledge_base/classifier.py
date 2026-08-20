import re

GENERAL_PATTERNS = [
    r"^hello\b",
    r"^hi\b",
    r"^hey\b",
    r"how are you",
    r"how are you doing",
    r"how are you today",
    r"what can you do",
    r"who are you",
    r"what are you",
    r"what is your purpose",
    r"what is the purpose of this app",
    r"what is the purpose of this application",
    r"good morning",
    r"good afternoon",
    r"good evening",
    r"thanks",
    r"thank you",
    r"bye\b",
]


def is_general_question(question: str) -> bool:

    question = question.lower().strip()

    for pattern in GENERAL_PATTERNS:

        if re.search(pattern, question):
            return True

    return False