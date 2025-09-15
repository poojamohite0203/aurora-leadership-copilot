from fastapi import APIRouter, HTTPException, Path, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.services.process_service import extract_and_create_meeting
from db.database import get_db
from db import models

router = APIRouter(tags=["Meeting"])

class TranscriptInput(BaseModel):
    transcript: str

@router.post("/extract")
def extract_meeting(input: TranscriptInput, db: Session = Depends(get_db)):
    """
    Extract structured meeting info from transcript,
    save to DB, and return full meeting data.
    """
    try:
        meeting_info = extract_and_create_meeting(input.transcript, db)
        return meeting_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_meeting_details(id: int = Path(...), db: Session = Depends(get_db)):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    action_items = db.query(models.Action_Item).filter(models.Action_Item.meeting_id == id).all()
    decisions = db.query(models.Decision).filter(models.Decision.meeting_id == id).all()
    blockers = db.query(models.Blocker).filter(models.Blocker.meeting_id == id).all()
    return {
        "id": meeting.id,
        "title": meeting.title,
        "summary": meeting.summary,
        "date": meeting.date,
        "participants": meeting.participants,
        "action_items": [a.__dict__ for a in action_items],
        "decisions": [d.__dict__ for d in decisions],
        "blockers": [b.__dict__ for b in blockers]
    }
