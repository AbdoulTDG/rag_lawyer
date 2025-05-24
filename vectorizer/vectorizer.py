from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from uuid import uuid4

# --- Config MongoDB ---
MONGO_URI = "mongodb://admin:pass123@15.237.211.7:27017/"
DB_NAME = "Rag"
COLLECTION_NAME = "rag"

# --- Connexion MongoDB ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# --- Récupération des chunks à vectoriser ---
documents = list(collection.find({"status": "ready_for_vectorization"}))

print(f"📄 {len(documents)} documents à vectoriser...")

# --- Modèle d'embedding ---
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# --- Connexion Qdrant ---
qdrant = QdrantClient(host="localhost", port=6333)
qdrant.recreate_collection(
    collection_name="rgpd_chunks",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# --- Création des vecteurs Qdrant ---
points = []
for doc in documents:
    chunk_text = doc["text"]
    vector = model.encode(chunk_text)

    payload = {
        "type": doc.get("type"),
        "index": doc.get("index"),
        "document_title": doc.get("document_title"),
        "source_file": doc.get("source_file"),
        "language": doc.get("language"),
        "text": chunk_text,
    }

    point = PointStruct(
        id=str(doc["_id"]),  # réutilise l’ID Mongo
        vector=vector.tolist(),
        payload=payload
    )
    points.append(point)

# --- Insertion dans Qdrant ---
qdrant.upsert(collection_name="rgpd_chunks", points=points)
print(f"✅ {len(points)} chunks vectorisés et insérés dans Qdrant.")
