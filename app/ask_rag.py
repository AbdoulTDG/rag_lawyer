# ask_rag.py

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import requests

# === CONFIGURATION ===
LLM_API_URL = "http://localhost:1234/v1/chat/completions"  # LM Studio API
COLLECTION_NAME = "rgpd_chunks"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# === INITIALISATION ===
print("🚀 Chargement du modèle d'embedding...")
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("🧠 Connexion à Qdrant...")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def ask_llm(context, question):
    """Envoie un prompt au LLM local via LM Studio."""
    prompt = f"""
Voici des extraits du RGPD :
{context}

En te basant uniquement sur ces extraits, réponds précisément à la question suivante :
{question}
"""

    response = requests.post(
        LLM_API_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": "local-model",  # Ignoré par LM Studio, mais requis
            "messages": [
                {"role": "system", "content": "Tu es un assistant juridique expert du RGPD."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur de LLM : {e}"

def retrieve_context(query, top_k=5):
    """Effectue une recherche sémantique dans Qdrant et retourne les textes associés."""
    query_vector = embedder.encode(query)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return "\n---\n".join([r.payload["text"] for r in results])

# === INTERFACE UTILISATEUR ===
if __name__ == "__main__":
    print("🧑‍💼 Système RAG RGPD prêt. Pose ta question (ou tape 'exit') 👇\n")

    while True:
        question = input("❓> ").strip()
        if question.lower() in ["exit", "quit"]:
            break

        print("🔍 Recherche des documents pertinents...")
        context = retrieve_context(question)

        print("\n🤖 Génération de la réponse...\n")
        response = ask_llm(context, question)
        print("💬 Réponse :\n")
        print(response)
        print("\n" + "=" * 60 + "\n")
