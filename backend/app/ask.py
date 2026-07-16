import json

from .utils.prompt import prompt
from .utils.llm import llm
from .services.chat_memory import (
    get_history,
    add_message
)


def get_answer(question: str, vector_db):

    if vector_db is None:
        raise Exception(
            "Vector database not found. Please upload documents first."
        )

    docs = vector_db.similarity_search(
        question,
        k=3
    )

    context = ""
    history = ""

    for chat in get_history():
        history += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )

    for i, doc in enumerate(docs, start=1):
        context += f"""
        ========== Context {i} ==========

        Context ID: {i}

        Document: {doc.metadata.get("doc_name", "Unknown")}
        Page: {doc.metadata.get("page", "?")}

        Content:
        {doc.page_content}

        ================================

        """

    messages = prompt.invoke({
        "history": history,
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    try:
        result = json.loads(response.content)

        used_contexts = result.get("used_contexts", [])

        sources = []

        for context_id in used_contexts:

            if isinstance(context_id, int) and 1 <= context_id <= len(docs):

                doc = docs[context_id - 1]

                citation = (
                    f"{doc.metadata.get('doc_name', 'Unknown')} "
                    f"(Page {doc.metadata.get('page', '?')})"
                )

                if citation not in sources:
                    sources.append(citation)

        answer = result.get(
            "answer",
            "I couldn't generate an answer."
        )

        add_message(question, answer)

        return {
            "answer": answer,
            "sources": sources
        }

    except json.JSONDecodeError:

        add_message(question, response.content)

        return {
            "answer": response.content,
            "sources": []
        }