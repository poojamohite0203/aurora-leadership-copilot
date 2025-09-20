from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import get_db
from api.services.rag_service import ask_question
from datetime import datetime

router = APIRouter(tags=["RAG"])

@router.get("/ask")
def ask(query: str = Query(..., description="Your natural language question")):
    return ask_question(query)