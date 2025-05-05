from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.kairos_core import KairosReflector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reflector = KairosReflector()

class Question(BaseModel):
    query: str
    mode: str = "default"

@app.post("/ask")
async def ask_kairos(question: Question):
    print("Received:", question.query, "| Mode:", question.mode)  # ⬅ debug
    answer = reflector.reflect(question.query, question.mode)
    return {"answer": answer}
