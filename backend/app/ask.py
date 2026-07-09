from utils.vector_store import load_vector_store
from utils.prompt import prompt
from utils.llm import llm

question = input("Ask: ")

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

print("\nAnswer:\n")
print(response.content)