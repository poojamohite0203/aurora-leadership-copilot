import os

try:
    import chromadb
    from chromadb.config import Settings

    # Detect if running on Streamlit Cloud
    ON_STREAMLIT_CLOUD = os.environ.get("STREAMLIT_SERVER") == "true"

    if ON_STREAMLIT_CLOUD:
        # In-memory Chroma (no persistence) for Streamlit Cloud
        persist_dir = None
    else:
        # Local disk persistence
        persist_dir = "./chromadb"

    client = chromadb.Client(Settings(
        persist_directory=persist_dir,
        anonymized_telemetry=False
    ))

    # Default collection
    collection = client.get_or_create_collection("default")

except Exception as e:
    print("⚠️ Chroma not available. Vector DB disabled:", e)
    client = None
    collection = None


def add_to_index(id: str, text: str, metadata: dict):
    if collection:
        collection.add(
            ids=[id],
            documents=[text],
            metadatas=[metadata]
        )

def query_index(query: str, n_results: int = 5):
    if collection:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    return None

def search(query: str, k: int = 5):
    """Search the vector DB using semantic similarity."""
    # Get embedding for the query
    embedding = model.encode(query).tolist()
    
    # Query the collection safely
    results = query_index(query=query, n_results=k)
    
    if results is None:
        return []  # Vector DB unavailable
    
    return results
