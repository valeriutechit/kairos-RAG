# rag/ingest.py
import os, glob
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "kairos_rag"
DATA_PATH = "./data"

# Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# OpenAI embedder
embedder = OpenAIEmbeddings(
    model="text-embedding-ada-002",  # безопасно укажем модель
    openai_api_key=OPENAI_API_KEY
)

def ingest_documents():
    # Создание коллекции
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    points = []

    # Чтение и разбиение файлов на абзацы
    for filepath in glob.glob(os.path.join(DATA_PATH, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 40]
        embeddings = embedder.embed_documents(paragraphs)

        for emb, text in zip(embeddings, paragraphs):
            points.append(PointStruct(
                id=str(uuid4()),
                vector=emb,
                payload={
                    "text": text,
                    "source": os.path.basename(filepath),
                }
            ))

    # ✅ Один вызов upsert
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Ingested {len(points)} chunks into Qdrant.")

if __name__ == "__main__":
    ingest_documents()
