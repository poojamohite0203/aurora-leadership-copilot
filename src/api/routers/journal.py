from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from api.services.process_service import extract_and_create_journal
from sqlalchemy.orm import Session
from db import models
from db.database import get_db

router = APIRouter(tags=["Journal"])

class JournalInput(BaseModel):
    text: str

@router.post("/extract")
def extract_journal(input: JournalInput, db: Session = Depends(get_db)):
    """
    Extract structured journal info from text,
    save to DB, and return full journal data.
    """
    try:
        journal_info = extract_and_create_journal(input.text, db)
        return journal_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_journal_details(id: int, db: Session = Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    action_items = db.query(models.Action_Item).filter(models.Action_Item.source == "journal", models.Action_Item.source_id == id).all()
    decisions = db.query(models.Decision).filter(models.Decision.source == "journal", models.Decision.source_id == id).all()
    blockers = db.query(models.Blocker).filter(models.Blocker.source == "journal", models.Blocker.source_id == id).all()
    return {
        "id": journal.id,
        "text": journal.text,
        "summary": journal.summary,
        "date": journal.date,
        "theme": getattr(journal, "theme", None),
        "strength": getattr(journal, "strength", None),
        "growth_area": getattr(journal, "growth_area", None),
        "action_items": [a.__dict__ for a in action_items],
        "decisions": [d.__dict__ for d in decisions],
        "blockers": [b.__dict__ for b in blockers]
    }