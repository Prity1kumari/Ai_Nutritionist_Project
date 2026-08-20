from typing import List


def format_context(documents: List) -> str:
    """
    Convert retrieved LangChain documents into a clean context string.
    """

    formatted_chunks = []

    for i, doc in enumerate(documents, start=1):

        source = doc.metadata.get("source", "Unknown Source")
        page = doc.metadata.get("page", "Unknown")

        chunk = f"""
=========================
Document {i}
Source : {source}
Page   : {page}
=========================

{doc.page_content}
"""

        formatted_chunks.append(chunk)

    return "\n".join(formatted_chunks)