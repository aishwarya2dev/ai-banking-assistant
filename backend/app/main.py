from fastapi import FastAPI ,HTTPException
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