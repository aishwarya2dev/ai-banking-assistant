from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)

    # Preserve document metadata for each chunk
    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        page = chunk.metadata.get("page", 0)

        chunk.metadata["doc_name"] = Path(source).name
        chunk.metadata["page"] = page + 1  # Convert 0-based page number to 1-based

    return chunks