import os
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

client = QdrantClient(host="localhost", port=6333)
client.recreate_collection(
    collection_name="rgpd_docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

point_id = 0
for filename in os.listdir("data"):
    if filename.endswith(".txt"):
        with open(f"data/{filename}", "r", encoding="utf-8") as f:
            text = f.read()
        
        chunks = splitter.split_text(text)
        vectors = model.encode(chunks)

        points = []
        for i, chunk in enumerate(chunks):
            payload = {
                "text": chunk,
                "source": filename,
                "chunk_id": i
            }
            points.append(PointStruct(id=point_id, vector=vectors[i].tolist(), payload=payload))
            point_id += 1

        client.upsert(collection_name="rgpd_docs", points=points)
        print(f"✅ {len(chunks)} chunks indexés depuis {filename}")
