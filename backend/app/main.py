from fastapi import FastAPI

app = FastAPI(title="AI Banking Assistant")

@app.get("/")
def home():
    return {"message": "AI Banking Assistant Running"}