from db.vector_store import search
from core.llm_utils import check_moderation

def search_items_service(query: str, k: int = 5):
    """
    Pure vector similarity retrieval.
    Takes a query, converts it to an embedding, and finds closest matches in the vector DB.
    Returns raw items with metadata - no LLM involved.
    """
    # Moderate Input
    ok, categories = check_moderation(query)
    if not ok:
        print(f"User input blocked due to: {categories}")
        raise ValueError(f"User input blocked due to: {categories}")
    
    results = search(query, k)
    
    # Transform the results to a more user-friendly format
    formatted_results = []
    if results and results.get("ids") and len(results["ids"]) > 0:
        ids = results["ids"][0]
        documents = results["documents"][0] if results.get("documents") else []
        metadatas = results["metadatas"][0] if results.get("metadatas") else []
        distances = results.get("distances", [None])[0] if results.get("distances") else []
        
        for i, doc_id in enumerate(ids):
            item = {
                "id": doc_id,
                "text": documents[i] if i < len(documents) else "",
                "metadata": metadatas[i] if i < len(metadatas) else {},
                "similarity_score": 1 - distances[i] if distances and i < len(distances) and distances[i] is not None else None
            }
            formatted_results.append(item)
    
    return {
        "query": query,
        "results": formatted_results,
        "total_results": len(formatted_results)
    }
