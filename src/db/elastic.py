import os
from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch
load_dotenv(find_dotenv())

# Get the Elasticsearch host and port from environment variables
es_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
es_port = os.getenv("ELASTICSEARCH_PORT", 9200)

# Initialize the Elasticsearch client
es = Elasticsearch([{"host": es_host, "port": es_port}])

# Example: Create an index
INDEX_NAME = "cybersecurity_reports"
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

# Example: Insert a document into Elasticsearch
document = {
    "report_id": "1234",
    "threat_level": "high",
    "description": "Detected potential phishing attempt",
}
es.index(index=INDEX_NAME, body=document)

# Example: Search for documents in Elasticsearch
response = es.search(index=INDEX_NAME, body={"query": {"match": {"threat_level": "high"}}})
print(response)