from langchain_community.document_loaders import PyPDFLoader
import os
import re


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents


def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


if __name__ == "__main__":

    pdf_folder = "../data/raw_pdfs"

    for file in os.listdir(pdf_folder):

        if file.endswith(".pdf"):

            path = os.path.join(pdf_folder, file)

            docs = load_pdf(path)

            print(f"\n📄 Loaded: {file}")
            print(f"Pages: {len(docs)}")

            print("\n🔹 Sample Content:\n")
            cleaned = clean_text(docs[0].page_content)

            print(cleaned[:1000])   