from pdf_loader import load_pdf
from chunking import create_chunks

pdf_path = "../../data/raw_pdfs/credit_card_tnc.pdf"

documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

print(f"\nTotal Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:5]):

    print("=" * 50)

    print(f"Chunk {i+1}")

    print(chunk.page_content[:300])

    print("\n")