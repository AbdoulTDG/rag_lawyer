from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.rag_chain import build_qa_chain

app = FastAPI()
qa_chain = build_qa_chain()

class QueryModel(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: QueryModel):
    response = qa_chain.run(query.question)
    return {"answer": response}
