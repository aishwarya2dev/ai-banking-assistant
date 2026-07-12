from pathlib import Path
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.app.ask import get_answer
from backend.app.ingest import ingest_documents

app = FastAPI(title="AI Banking Assistant")

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parents[2]

# Directory to store uploaded PDFs
UPLOAD_DIR = BASE_DIR / "data" / "raw_pdfs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Banking Assistant Running"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        answer = get_answer(request.question)

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunk_count = ingest_documents(file_path)

        return {
            "message": "PDF uploaded successfully.",
            "filename": file.filename,
            "chunks_indexed": chunk_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )