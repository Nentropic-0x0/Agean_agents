from langchain.embeddings import OpenAIEmbeddings
from chromadb import loader, Chroma



vectorstore = Chroma(
    collection_name="rag-chroma",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./db/vector/data/chroma_langchain_db", 
)

vectorstore.add_documents(documents=docs)
retriever = vectorstore.as_retriever()