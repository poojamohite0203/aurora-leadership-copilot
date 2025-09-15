from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from api.services.process_service import extract_and_create_clip
from sqlalchemy.orm import Session
from src.db import models, get_db

router = APIRouter(prefix="/clips", tags=["clips"])

class ClipInput(BaseModel):
    text: str

@router.post("/extract")
def extract_clip(input: ClipInput):
    """
    Extract structured clip info from text,
    save to DB, and return full clip data.
    """
    try:
        clip_info = extract_and_create_clip(input.text)
        return clip_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_clip_details(id: int, db: Session = Depends(get_db)):
    clip = db.query(models.Clip).filter(models.Clip.id == id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    action_items = db.query(models.Action_Item).filter(models.Action_Item.source == "clip", models.Action_Item.source_id == id).all()
    decisions = db.query(models.Decision).filter(models.Decision.source == "clip", models.Decision.source_id == id).all()
    blockers = db.query(models.Blocker).filter(models.Blocker.source == "clip", models.Blocker.source_id == id).all()
    return {
        "id": clip.id,
        "text": clip.text,
        "summary": clip.summary,
        "date": clip.date,
        "action_items": [a.__dict__ for a in action_items],
        "decisions": [d.__dict__ for d in decisions],
        "blockers": [b.__dict__ for b in blockers]
    }