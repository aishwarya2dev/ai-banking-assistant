from pathlib import Path

from .services.pdf_loader import load_pdf
from .services.chunking import create_chunks
from .utils.vector_store import create_vector_store

BASE_DIR = Path(__file__).resolve().parents[2]

def ingest_documents(pdf_path: Path):

    documents = load_pdf(pdf_path)
    chunks = create_chunks(documents)
    create_vector_store(chunks)

    return len(chunks)


if __name__ == "__main__":
    pdf_path = BASE_DIR / "data" / "raw_pdfs" / "credit_card_tnc.pdf"
    count = ingest_documents(pdf_path)
    print(f"Indexed {count} chunks successfully!")