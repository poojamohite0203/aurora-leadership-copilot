import os
from sentence_transformers import SentenceTransformer

try:
    import chromadb
    from chromadb.config import Settings

    # Detect if running on Streamlit Cloud
    ON_STREAMLIT_CLOUD = os.environ.get("STREAMLIT_SERVER") == "true"

    if ON_STREAMLIT_CLOUD:
        # In-memory Chroma (no persistence) for Streamlit Cloud
        print("On Streamlit cloud")
        persist_dir = None
    else:
        # Local disk persistence
        persist_dir = "./.chroma"
        print("ChromaDB persist directory:", persist_dir)


    client = chromadb.Client(Settings(
        persist_directory=persist_dir,
        anonymized_telemetry=False
    ))

    # Default collection
    collection = client.get_or_create_collection("knowledge_base")
    model = SentenceTransformer("all-MiniLM-L6-v2")

except Exception as e:
    print("⚠️ Chroma not available. Vector DB disabled:", e)
    client = None
    collection = None


def add_to_index(id: str, text: str, metadata: dict):
    embedding = model.encode(text).tolist()
    if collection:
        collection.add(
            ids=[id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding]
        )

def query_index(query: str, n_results: int = 5):
    if collection:
         # Get embedding for the query
        embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results
    return None

def search(query: str, k: int = 5):
    """Search the vector DB using semantic similarity."""

    # Query the collection safely
    results = query_index(query=query, n_results=k)
    
    if results is None:
        return []  # Vector DB unavailable
    
    return results
