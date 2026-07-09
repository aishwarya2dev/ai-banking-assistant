from pathlib import Path

from services.pdf_loader import load_pdf
from services.chunking import create_chunks
from utils.vector_store import create_vector_store

BASE_DIR = Path(__file__).resolve().parents[2]
pdf_path = BASE_DIR / "data" / "raw_pdfs" / "credit_card_tnc.pdf"


documents = load_pdf(pdf_path)
chunks = create_chunks(documents)
vector_db = create_vector_store(chunks)

print(f"Indexed {len(chunks)} chunks successfully!")



