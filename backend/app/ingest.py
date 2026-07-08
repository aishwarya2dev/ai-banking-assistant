from pathlib import Path

from services.pdf_loader import load_pdf
from services.chunking import create_chunks
from utils.vector_store import create_vector_store
from langchain_community.vectorstores import FAISS
from utils.embeddings import embedding_model

BASE_DIR = Path(__file__).resolve().parents[2]
pdf_path = BASE_DIR / "data" / "raw_pdfs" / "credit_card_tnc.pdf"

def load_vector_store():
    return FAISS.load_local(
        "vectorstore/faiss_db",
        embedding_model,
        allow_dangerous_deserialization=True
    )


documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

vector_db = create_vector_store(chunks)

print(f"Indexed {len(chunks)} chunks successfully!")



