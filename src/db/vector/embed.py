import qdrant_client
from openai import OpenAI
from qdrant_client.models import PointStruct

# DECIDE HOW DATA COMES IN

def get_embedding(text, model="text-embedding-3-small"):
   openai_client = OpenAI()
   text = text.replace("\n", " ")
   return openai_client.embeddings.create(input = [text], model=model).data[0].embedding
 
def embeddings(data, model="text-embedding-3-small"):
    
    embedding_model = model
    result = openai_client.create(input=data, model=embedding_model)

    # Converting the model outputs to Qdrant points
    points = [
        PointStruct(
            id=idx,
            vector=data.embedding,
            payload={"text": text},
        )
        for idx, (data, text) in enumerate(zip(result.data, data))
    ]
    
    return points

def search_qdrant(query, client, collection_name, model="text-embedding-3-small"):
    client.search(
    collection_name=collection_name,
    query_vector=client.embeddings.create(
        input=[query],
        model=model,
    )
    .data[0]
    .embedding,
)