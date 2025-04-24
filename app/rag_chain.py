from pymongo import MongoClient
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

def build_qa_chain():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    collection_name = os.getenv("COLLECTION_NAME")
    text_field = os.getenv("TEXT_FIELD", "texte")

    # MongoDB
    client = MongoClient(mongo_uri)
    collection = client[db_name][collection_name]
    texts = [doc[text_field] for doc in collection.find({}, {text_field: 1}) if text_field in doc]

    # Split + embeddings
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for text in texts for chunk in splitter.split_text(text)]
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(temperature=0)
    
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
