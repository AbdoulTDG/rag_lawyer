from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Connexion
client = QdrantClient(host="localhost", port=6333)

# Modèle
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

while True:
    query = input("\n📝 Tape ta question (ou 'exit' pour quitter) :\n> ")
    if query.lower() in ["exit", "quit"]:
        break

    query_vector = model.encode(query)

    results = client.search(
        collection_name="rgpd_chunks",
        query_vector=query_vector,
        limit=3
    )

    print("\n🔍 Résultats pertinents :\n")
    for res in results:
        print("→", res.payload["text"], "\n")
