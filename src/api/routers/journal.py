from fastapi import APIRouter, HTTPException, Depends, Query, Body
from api.services.process_service import extract_and_create_journal
from sqlalchemy.orm import Session
from db import crud
from db.database import get_db
from typing import Optional

router = APIRouter(tags=["Journal"])

@router.get("")
def get_all_journals(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of journals returned")
):
    """
    Return all journals without nested action items, decisions, and blockers.
    Optional limit parameter to control the number of results.
    """
    try:
        return crud.get_all_journals(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
def extract_journal(text: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db)):
    """
    Extract structured journal info from raw text.
    Just paste your text directly - no JSON formatting needed!
    """
    try:
        journal_info = extract_and_create_journal(text, db)
        return journal_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_journal_details(id: int, db: Session = Depends(get_db)):
    """Get a specific journal by ID without nested data"""
    journal = crud.get_journal_by_id(db, id)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    return {
        "id": journal.id,
        "text": journal.text,
        "summary": journal.summary,
        "date": journal.date,
        "theme": journal.theme,
        "strength": journal.strength,
        "growth_area": journal.growth_area
    }