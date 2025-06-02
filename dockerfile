FROM python:3.10-slim

WORKDIR /app


# COPY rag_chain.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.rag_chain:app", "--host", "0.0.0.0", "--port", "8000"]
