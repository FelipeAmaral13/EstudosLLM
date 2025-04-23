import os
import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="NormasInternas")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

def index_documents(docs: list[str]):
    embeddings = openai_ef(docs)
    collection.add(
        documents=docs,
        ids=[f"norma{i}" for i in range(len(docs))],
        embeddings=embeddings
    )

def query_normas(query: str, n=3) -> list[str]:
    result = collection.query(query_texts=[query], n_results=n)
    return result["documents"][0] if result["documents"] else ["Nenhuma norma encontrada."]
