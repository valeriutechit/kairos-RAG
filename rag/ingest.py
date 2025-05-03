# rag/ingest.py
import os, glob
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from langchain.embeddings import OpenAIEmbeddings
from uuid import uuid4

QDRANT_URL = os.getenv("QDRANT_URL", "https://your-url.qdrant.io")  # заменишь в .env
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "your-api-key")
COLLECTION_NAME = "kairos_rag"
DATA_PATH = "./data"

# Подключение к Qdrant Cloud
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Инициализация эмбеддингов
embedder = OpenAIEmbeddings()

def ingest_documents():
    # Создание коллекции, если не существует
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    # Обработка .md файлов из папки data/
    for filepath in glob.glob(os.path.join(DATA_PATH, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Получение эмбеддинга текста
        embedding = embedder.embed_query(content)

        # Добавление в Qdrant как одну точку (Point)
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "text": content,
                        "source": os.path.basename(filepath),
                    }
                )
            ]
        )
    print("✅ Ingestion to Qdrant complete")

if __name__ == "__main__":
    ingest_documents()
