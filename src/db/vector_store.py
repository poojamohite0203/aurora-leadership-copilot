import os
try:
    import chromadb
    from chromadb.config import Settings

    # Always use in-memory vector store (no persistence)
    print("🗑️ Using in-memory ChromaDB (no persistence, data lost on restart)")
    client = chromadb.Client(Settings(
        persist_directory=None,
        anonymized_telemetry=False
    ))

    # Default collection
    collection = client.get_or_create_collection("knowledge_base")
    print("✅ ChromaDB and SentenceTransformer loaded successfully")

except Exception as e:
    print(f"⚠️ ChromaDB not available. Vector search disabled: {e}")
    client = None
    collection = None
    model = None

def add_to_index(id: str, text: str, metadata: dict):
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    # if not model or not collection:
    #     print("⚠️ Vector DB not available - skipping indexing")
    #     return
    
    # try:
    #     embedding = model.encode(text).tolist()
    #     collection.add(
    #         ids=[id],
    #         documents=[text],
    #         metadatas=[metadata],
    #         embeddings=[embedding]
    #     )
    #     print(f"✅ Added to index: {id}")
    # except Exception as e:
    #     print(f"❌ Error adding to index: {e}")
    print("Not adding to index")

def query_index(query: str, n_results: int = 5):
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    # if not model or not collection:
    #     return None
        
    # try:
    #     embedding = model.encode(query).tolist()
    #     results = collection.query(
    #         query_embeddings=[embedding],
    #         n_results=n_results
    #     )
    #     return results
    # except Exception as e:
    #     print(f"❌ Error querying index: {e}")
    #     return None
    return []

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