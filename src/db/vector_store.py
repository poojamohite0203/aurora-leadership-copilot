import os
try:
    import chromadb
    from chromadb.config import Settings

    # Detect deployment environment
    IS_RENDER = os.environ.get("RENDER") is not None
    IS_STREAMLIT_CLOUD = "/mount/src" in os.getcwd()
    
    if IS_RENDER:
        # Render.com - use persistent disk storage in /app/data
        persist_dir = "/app/data/.chroma"
        os.makedirs(persist_dir, exist_ok=True)
        print(f"🚀 Render.com - ChromaDB persist directory: {persist_dir}")
        client = chromadb.PersistentClient(path=persist_dir)
        
    elif IS_STREAMLIT_CLOUD:
        # Streamlit Cloud - in-memory only
        print("☁️ Streamlit Cloud - using in-memory vector store")
        client = chromadb.Client(Settings(
            persist_directory=None,
            anonymized_telemetry=False
        ))
        
    else:
        # Local development with persistence
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        persist_dir = os.path.join(project_root, ".chroma")
        print(f"💻 Local development - ChromaDB persist directory: {persist_dir}")
        client = chromadb.PersistentClient(path=persist_dir)

    # Default collection
    collection = client.get_or_create_collection("knowledge_base")
    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    print("✅ ChromaDB and SentenceTransformer loaded successfully")

except Exception as e:
    print(f"⚠️ ChromaDB not available. Vector search disabled: {e}")
    client = None
    collection = None
    model = None

def add_to_index(id: str, text: str, metadata: dict):
    from sentence_transformers import SentenceTransformer
    if not model or not collection:
        print("⚠️ Vector DB not available - skipping indexing")
        return
    
    try:
        embedding = model.encode(text).tolist()
        collection.add(
            ids=[id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding]
        )
        print(f"✅ Added to index: {id}")
    except Exception as e:
        print(f"❌ Error adding to index: {e}")

def query_index(query: str, n_results: int = 5):
    if not model or not collection:
        return None
        
    try:
        embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"❌ Error querying index: {e}")
        return None

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
    return results if results else []