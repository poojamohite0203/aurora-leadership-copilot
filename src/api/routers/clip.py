from fastapi import APIRouter, HTTPException, Depends, Query, Body
from api.services.process_service import extract_and_create_clip
from sqlalchemy.orm import Session
from db import crud
from db.database import get_db
from typing import Optional

router = APIRouter(tags=["Clip"])

@router.get("")
def get_all_clips(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of clips returned")
):
    """
    Return all clips without nested action items, decisions, and blockers.
    Optional limit parameter to control the number of results.
    """
    try:
        return crud.get_all_clips(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
def extract_clip(text: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db)):
    """
    Extract structured clip info from raw text.
    Just paste your text directly - no JSON formatting needed!
    """
    try:
        clip_info = extract_and_create_clip(text, db)
        return clip_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_clip_details(id: int, db: Session = Depends(get_db)):
    """Get a specific clip by ID without nested data"""
    clip = crud.get_clip_by_id(db, id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    return {
        "id": clip.id,
        "text": clip.text,
        "summary": clip.summary,
        "date": clip.date
    }