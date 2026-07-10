from .utils.vector_store import load_vector_store
from .utils.prompt import prompt
from .utils.llm import llm

# Load the vector database once when the application starts
try:
    vector_db = load_vector_store()
except Exception:
    vector_db = None


def get_answer(question: str) -> str:
    

    if vector_db is None:
        raise Exception(
            "Vector database not found. Please ingest the documents first."
        )

    docs = vector_db.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":
    question = input("Ask: ")
    answer = get_answer(question)

    print("\nAnswer:\n")
    print(answer)