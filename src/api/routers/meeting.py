from fastapi import APIRouter, HTTPException, Path, Depends, Query, Body
from sqlalchemy.orm import Session
from api.services.process_service import extract_and_create_meeting
from api.services.get_service import get_all_meetings_service, get_meeting_details_service
from db.database import get_db
from db import crud
from typing import Optional

router = APIRouter(tags=["Meeting"])

@router.get("")
def get_all_meetings(
    db: Session = Depends(get_db),
    from_date: Optional[str] = Query(None, description="Filter meetings from this date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Filter meetings to this date (YYYY-MM-DD)")
):
    """
    Return all meetings without nested action items, decisions, and blockers.
    Optional date filtering with from_date and to_date query parameters.
    """
    try:
        return get_all_meetings_service(db, from_date, to_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extract")
def extract_meeting(transcript: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db)):
    """
    Extract structured meeting info from raw transcript text.
    Just paste your meeting transcript directly - no JSON formatting needed!
    """
    try:
        meeting_info = extract_and_create_meeting(transcript, db)
        return meeting_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_meeting_details(id: int = Path(...), db: Session = Depends(get_db)):
    """Get a specific meeting by ID without nested data"""
    meeting = get_meeting_details_service(db, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
