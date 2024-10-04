import os
from typing import Any, Dict

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Elasticsearch configuration
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_HOST = "elasticsearch"  # This should match the service name in docker-compose
ELASTIC_PORT = "9200"

# Initialize Elasticsearch client
es = Elasticsearch(
    [f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"],
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

class Document(BaseModel):
    index: str
    doc_type: str
    body: Dict[str, Any]

class SearchQuery(BaseModel):
    index: str
    query: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "Welcome to the ELK Stack API"}

@app.get("/health")
async def health_check():
    if es.ping():
        return {"status": "healthy", "elasticsearch": "connected"}
    else:
        raise HTTPException(status_code=503, detail="Elasticsearch is not available")

@app.post("/index")
async def index_document(document: Document):
    try:
        response = es.index(index=document.index, doc_type=document.doc_type, body=document.body)
        return {"message": "Document indexed successfully", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_documents(search_query: SearchQuery):
    try:
        response = es.search(index=search_query.index, body=search_query.query)
        return {"results": response['hits']['hits']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indices")
async def list_indices():
    try:
        indices = es.indices.get_alias().keys()
        return {"indices": list(indices)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)