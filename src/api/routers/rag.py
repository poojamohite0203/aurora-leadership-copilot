# src/routes/rag.py
from fastapi import APIRouter, Query
from api.services.rag_service import ask_question

router = APIRouter(tags=["RAG"])

@router.get("/ask")
def ask(query: str = Query(..., description="Your natural language question")):
    return ask_question(query)