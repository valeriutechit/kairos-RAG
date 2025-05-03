# rag/query.py
import os
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Подгружает переменные из .env

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "kairos_rag"

# Инициализация клиента Qdrant
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Инициализация embedder и OpenAI LLM
embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(query: str, top_k: int = 3) -> str:
    # Преобразуем вопрос в вектор
    query_vector = embedder.embed_query(query)

    # Ищем наиболее релевантные документы в Qdrant
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
    )

    # Извлекаем тексты найденных фрагментов
    contexts = [hit.payload["text"] for hit in hits]

    # Формируем prompt
    context_str = "\n---\n".join(contexts)
    prompt = f"""Ответь на вопрос на основе контекста ниже. Если не уверен — скажи честно.
    
Контекст:
{context_str}

Вопрос:
{query}

Ответ:"""

    # Отправляем prompt в OpenAI
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return completion.choices[0].message.content.strip()

# Для теста из CLI
if __name__ == "__main__":
    query = input("❓ Введи вопрос: ")
    answer = ask_question(query)
    print("\n💬 Ответ:\n", answer)
