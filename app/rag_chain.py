from pymongo import MongoClient
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA,LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline,Ollama
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
import tqdm
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline,AutoModelForSeq2SeqLM

load_dotenv()

def build_qa_chain():

    # Paramètres Qdrant
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rgpd_chunks")

    # Connexion à la BDD vectorielle
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    
    # Vectorisation des textes
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Connexion au vectorstore avec LangChain
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embeddings
    )
    retriever = vectorstore.as_retriever()
    # llm = ChatOpenAI(temperature=0)
    # llm_ollama = Ollama(model="mistral")
    llm_ollama = Ollama(model="llma3",base_url="http://ollama:11434")


    # Construction de la chaîne QA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_ollama,
        retriever=retriever,
        # chain_type="stuff",  # important
        # chain_type_kwargs={"prompt": prompt_template}
    )

    
    return qa_chain

# RetrievalQA.from_chain_type(llm=llm, retriever=retriever)