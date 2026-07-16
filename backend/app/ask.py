from .utils.prompt import prompt
from .utils.llm import llm


def get_answer(question: str, vector_db) -> str:

    if vector_db is None:
        raise Exception(
            "Vector database not found. Please upload documents first."
        )

    docs = vector_db.similarity_search(
        question,
        k=3
    )

    sources = []
    for doc in docs:
        doc_name = doc.metadata.get("doc_name", "Unknown")
        page = doc.metadata.get("page", "?")

        citation = f"{doc_name} (Page {page})"

        if citation not in sources:
            sources.append(citation)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "sources": sources
    }