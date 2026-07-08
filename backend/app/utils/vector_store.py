from langchain_community.vectorstores import FAISS
from utils.embeddings import embedding_model


def create_vector_store(chunks):
    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    vector_db.save_local("vectorstore/faiss_db")

    return vector_db
