from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)

    return chunks