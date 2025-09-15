from fastapi import APIRouter, HTTPException, Path, Depends, Query, Body
from sqlalchemy.orm import Session
from api.services.process_service import extract_and_create_meeting
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
        meetings = crud.get_all_meetings(db, from_date, to_date)

        return [
            {
                "id": m.id,
                "title": m.title,
                "date": m.date,
                "participants": m.participants,
                "summary": m.summary,
                "action_items": [
                    {"id": a.id, "description": a.description, "due_date": a.due_date}
                    for a in m.action_items
                ],
                "decisions": [
                    {"id": d.id, "description": d.description, "other_options": d.other_options}
                    for d in m.decisions
                ],
                "blockers": [
                    {"id": b.id, "description": b.description}
                    for b in m.blockers
                ]
            }
            for m in meetings
    ]
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
    meeting = crud.get_meeting_by_id(db, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "id": meeting.id,
        "title": meeting.title,
        "summary": meeting.summary,
        "date": meeting.date,
        "participants": meeting.participants,
        "action_items": [
            {"id": a.id, "description": a.description, "due_date": a.due_date}
            for a in meeting.action_items
        ],
        "decisions": [
            {"id": d.id, "description": d.description, "other_options": d.other_options}
            for d in meeting.decisions
        ],
        "blockers": [
            {"id": b.id, "description": b.description}
            for b in meeting.blockers
        ]
    }
