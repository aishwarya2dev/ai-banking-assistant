from pathlib import Path
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.app.ask import get_answer
from backend.app.ingest import ingest_documents
from backend.app.utils.vector_store import load_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        app.state.vector_db = load_vector_store()
        print("✅ Vector database loaded successfully.")

    except Exception:
        app.state.vector_db = None
        print("⚠️ No vector database found.")

    yield


app = FastAPI(
    title="AI Banking Assistant",
    lifespan=lifespan
)

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "raw_pdfs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Banking Assistant Running"
    }


@app.post("/ask")
def ask_question(request: QueryRequest):

    try:

        answer = get_answer(
            request.question,
            app.state.vector_db
        )

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

        app.state.vector_db = load_vector_store()

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