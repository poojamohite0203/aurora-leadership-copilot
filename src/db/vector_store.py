# Ensure environment variables are loaded for both local and Docker
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
from langsmith import traceable
try:
    import chromadb
    from chromadb.config import Settings

    # Use environment variable for ChromaDB persist directory
    persist_dir = os.environ.get("CHROMA_DIR", "./data/.chroma")  # Use relative path by default
    IS_RENDER = os.environ.get("RENDER") is not None
    IS_STREAMLIT_CLOUD = "/mount/src" in os.getcwd()
    
    if IS_RENDER:
        # Render.com - use persistent disk storage
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
        os.makedirs(persist_dir, exist_ok=True)
        print(f"💻 Local development - ChromaDB persist directory: {persist_dir}")
        client = chromadb.PersistentClient(path=persist_dir)

    # Default collection
    collection = client.get_or_create_collection("knowledge_base")
    print("✅ ChromaDB loaded successfully")

except Exception as e:
    print(f"⚠️ ChromaDB not available. Vector search disabled: {e}")
    client = None
    collection = None
    model = None

# Load OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set. Check your .env or environment variables.")
openai_client = OpenAI(api_key=api_key)
@traceable
def get_openai_embedding(text):
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error getting OpenAI embedding: {e}")
        return None
@traceable
def add_to_index(id: str, text: str, metadata: dict):
    embedding = get_openai_embedding(text)
    if not embedding or not collection:
        print("⚠️ Vector DB not available or embedding failed - skipping indexing")
        return
    try:
        collection.add(
            ids=[id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding]
        )
        print(f"✅ Added to index: {id}")
    except Exception as e:
        print(f"❌ Error adding to index: {e}")
@traceable
def query_index(query: str, n_results: int = 5):
    embedding = get_openai_embedding(query)
    if not embedding or not collection:
        return None
    try:
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
    results = query_index(query=query, n_results=k)
    return results if results else []