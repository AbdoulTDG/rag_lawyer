
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import StreamingResponse
import json
import time

load_dotenv()

# === CONFIGURATION ===
LLM_API_URL =os.getenv("LLM_API_URL") 
COLLECTION_NAME =os.getenv("QDRANT_COLLECTION_NAME")
QDRANT_HOST =os.getenv("QDRANT_HOST") 
QDRANT_PORT =os.getenv("QDRANT_PORT")

# === INITIALISATION ===
app = FastAPI()
# Chargement du modèle d'embedding
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Connexion à Qdrant
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


class QuestionRequest(BaseModel):
    question: str


def stream_llm(context, question):
    prompt = f"""
Voici des extraits du RGPD :
{context}

En te basant uniquement sur ces extraits, réponds précisément à la question suivante :
{question}
"""
    def generate():
        with requests.post(
            LLM_API_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "temperature": 0.2,
                "stream": True
            },
            stream=True
        ) as response:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))["response"]
                        yield chunk
                    except:
                        pass
    return StreamingResponse(generate(), media_type="text/plain")


def retrieve_context(query, top_k=10):
    """Effectue une recherche sémantique dans Qdrant et retourne les textes associés"""
    query_vector = embedder.encode(query)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return "\n---\n".join([r.payload["text"][:300] for r in results])


@app.post("/ask")
def ask_question(data: QuestionRequest):
    t0 = time.time()
    context = retrieve_context(data.question)
    t1 = time.time()
    answer = stream_llm(context, data.question)
    t2 = time.time()

    print(f"Retrieval time: {t1 - t0:.2f}s")
    print(f"LLM generation time: {t2 - t1:.2f}s")

    return answer
