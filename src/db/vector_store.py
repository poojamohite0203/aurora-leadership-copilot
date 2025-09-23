import os
from sentence_transformers import SentenceTransformer

try:
    import chromadb
    from chromadb.config import Settings

    # Better detection for Streamlit Cloud
    ON_STREAMLIT_CLOUD = (
        os.environ.get("STREAMLIT_CLOUD") == "true" or 
        os.environ.get("STREAMLIT_SERVER") == "true" or
        "/mount/src" in os.getcwd()  # Streamlit Cloud uses /mount/src
    )

    if ON_STREAMLIT_CLOUD:
        # In-memory Chroma (no persistence) for Streamlit Cloud
        print("On Streamlit Cloud - using in-memory vector store")
        client = chromadb.Client(Settings(
            persist_directory=None,
            anonymized_telemetry=False
        ))
    else:
        # Local disk persistence - use absolute path to project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        persist_dir = os.path.join(project_root, ".chroma")
        print("Local development - ChromaDB persist directory:", persist_dir)
        
        # IMPORTANT: Use PersistentClient for disk persistence
        client = chromadb.PersistentClient(path=persist_dir)

    # Default collection
    collection = client.get_or_create_collection("knowledge_base")
    model = SentenceTransformer("all-MiniLM-L6-v2")

except Exception as e:
    print("⚠️ Chroma not available. Vector DB disabled:", e)
    client = None
    collection = None
    model = None

def add_to_index(id: str, text: str, metadata: dict):
    if not model or not collection:
        return
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[id],
        documents=[text],
        metadatas=[metadata],
        embeddings=[embedding]
    )
    print(f"Added to index: {id}")  # Debug

def query_index(query: str, n_results: int = 5):
    if not model or not collection:
        return None
    # Get embedding for the query
    embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results

def search(query: str, k: int = 5):
    """Search the vector DB using semantic similarity."""

    # Debugging 
    # try:
    #     # List all collections
    #     collections = client.list_collections()
    #     print(f"Available collections: {[c.name for c in collections]}")
        
    #     # Check ALL collections for data
    #     for coll in collections:
    #         count = coll.count()
    #         print(f"Collection '{coll.name}' has {count} items")
            
    # except Exception as e:
    #     print(f"Debug error: {e}")
    
    # Query the collection safely
    results = query_index(query=query, n_results=k)
    
    if results is None:
        return []  # Vector DB unavailable
    
    return results