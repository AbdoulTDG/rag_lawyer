# from pymongo import MongoClient
# from langchain.schema import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA,LLMChain
# from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama #HuggingFacePipeline
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
# import tqdm
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline,AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer

load_dotenv()

# ask_rag.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import StreamingResponse
import json
import time

# === CONFIGURATION ===
LLM_API_URL = "http://ollama:11434/api/generate"  # Nom du conteneur Docker
COLLECTION_NAME = "rgpd_chunks"
QDRANT_HOST = "qdrant"
QDRANT_PORT = 6333

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

    #return {"answer": answer} #old version to avoid async_generator error
    return answer


# def build_qa_chain():

#     # Paramètres Qdrant
#     QDRANT_HOST="localhost" #os.getenv("QDRANT_HOST", "localhost")
#     QDRANT_PORT= 6333 #int(os.getenv("QDRANT_PORT", 6333))
#     QDRANT_COLLECTION_NAME="rgpd_chunks"#os.getenv("QDRANT_COLLECTION_NAME", "rgpd_chunks")


#     LLM_API_URL = "http://localhost:11434/api/generate" 


#     # Connexion à la BDD vectorielle
#     qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    
#     # Vectorisation des textes
#     # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     embeddings=SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
#     # Connexion au vectorstore avec LangChain
#     vectorstore = Qdrant(
#         client=qdrant_client,
#         collection_name=QDRANT_COLLECTION_NAME,
#         embeddings=embeddings
#     )
#     retriever = vectorstore.as_retriever()
#     # llm = ChatOpenAI(temperature=0)
#     # llm_ollama = Ollama(model="mistral")
#     llm_ollama = Ollama(model="llma3",base_url="http://ollama:11434")


#     # Construction de la chaîne QA
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm_ollama,
#         retriever=retriever,
#         # chain_type="stuff",  # important
#         # chain_type_kwargs={"prompt": prompt_template}
#     )

    
#     return qa_chain

# RetrievalQA.from_chain_type(llm=llm, retriever=retriever)