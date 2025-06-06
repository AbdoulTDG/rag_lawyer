from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()
# --- Config MongoDB ---
mongo_uri =os.getenv("MONGO_URI") #"mongodb://admin:pass123@15.237.211.7:27017/" 
db_name = os.getenv("DB_NAME") #"Rag"
collection_name =os.getenv("COLLECTION_NAME") #"rag"
# text_field = os.getenv("TEXT_FIELD", "texte")

# --- Connexion MongoDB ---
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# --- Récupération des chunks à vectoriser ---
documents = list(collection.find({"status": "ready_for_vectorization"}))

print(f"{len(documents)} documents à vectoriser...")

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
