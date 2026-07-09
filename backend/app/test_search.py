from utils.vector_store import load_vector_store

db = load_vector_store()
query = "minimum balance"

results = db.similarity_search(query, k=3)

for i, doc in enumerate(results, start=1):
    print("=" * 50)
    print(f"Result {i}")
    print(doc.page_content)
    print()