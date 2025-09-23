from fastapi import APIRouter
from api.services.search_service import search_items_service

router = APIRouter(tags=["Search"])

@router.get("/search")
def search_items(query: str, k: int = 5):
    """
    Pure vector similarity retrieval.
    Takes a query, converts it to an embedding, and finds closest matches in the vector DB.
    Returns raw items with metadata - no LLM involved.
    """

    return search_items_service(query, k)
