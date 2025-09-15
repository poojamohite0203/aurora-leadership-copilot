import chromadb
from sentence_transformers import SentenceTransformer

# Persistent Chroma client (saved in .chroma folder)
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_or_create_collection("knowledge_base")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def add_to_index(id: str, text: str, metadata: dict):
    """Add a document (clip/journal/meeting) to Chroma index"""
    embedding = model.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[id],
        metadatas=[metadata],
    )


def search(query: str, k: int = 5):
    """Search the vector DB using semantic similarity"""
    embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return results
