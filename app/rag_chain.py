from pymongo import MongoClient
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os

def build_qa_chain():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    collection_name = os.getenv("COLLECTION_NAME")
    text_field = os.getenv("TEXT_FIELD", "texte")

    # Connexion à MongoDB
    client = MongoClient(mongo_uri)
    collection = client[db_name][collection_name]
    texts = [doc[text_field] for doc in collection.find({}, {text_field: 1}) if text_field in doc]

    # Séparation des textes
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for text in texts for chunk in splitter.split_text(text)]
    
    # Vectorisation des textes
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    retriever = vectorstore.as_retriever()
    # llm = ChatOpenAI(temperature=0)
    llm_ollama = Ollama(model="mistral")
    
    return RetrievalQA.from_chain_type(llm=llm_ollama, retriever=retriever)
