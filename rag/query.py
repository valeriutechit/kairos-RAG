import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv

from backend.kairos_core import reflect

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "kairos_rag"

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
embedder = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(query: str, top_k: int = 3, fallback_mode: str = "default") -> str:
    try:
        query_vector = embedder.embed_query(query)
        hits = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )
        contexts = [hit.payload["text"] for hit in hits if "text" in hit.payload]

        if not contexts:
            return reflect(query, mode=fallback_mode)

        context_str = "\n---\n".join(contexts)
        prompt = f"""Answer the question based on the context below. If you're unsure — say so honestly.

Context:
{context_str}

Question:
{query}

Answer:"""

        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        return f"Error processing query: {str(e)}"

if __name__ == "__main__":
    q = input("❓ Enter question: ")
    print("\n💬", ask_question(q))
