from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.ask import get_answer

app = FastAPI(title="AI Banking Assistant")


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Banking Assistant Running"}


@app.post("/ask")
def ask_question(request: QueryRequest):

    answer = get_answer(request.question)
    return {
        "answer": answer
    }