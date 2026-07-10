from .utils.vector_store import load_vector_store
from .utils.prompt import prompt
from .utils.llm import llm


def get_answer(question: str) -> str:
    
    vector_db = load_vector_store()

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