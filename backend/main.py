from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.query import ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str
    mode: str = "default"

@app.post("/ask")
async def ask_kairos(question: Question):
    print("🧠 Received:", question.query, "| Mode:", question.mode)
    answer = ask_question(question.query, fallback_mode=question.mode)
    return {"answer": answer}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.head("/health")
async def health_check_head():
    return Response(status_code=200)