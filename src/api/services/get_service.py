from sqlalchemy.orm import Session
from typing import Optional
from db import crud
from datetime import datetime

def get_all_meetings_service(db: Session, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """
    Return all meetings without nested action items, decisions, and blockers.
    Optional date filtering with from_date and to_date query parameters.
    This mirrors the logic from the router but is now reusable.
    """
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

def get_meeting_details_service(db: Session, meeting_id: int):
    meeting = crud.get_meeting_by_id(db, meeting_id)
    if not meeting:
        return None
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

# --- Clips ---
def get_all_clips_service(db: Session, limit: Optional[int] = None):
    return crud.get_all_clips(db, limit)

def get_clip_details_service(db: Session, clip_id: int):
    clip = crud.get_clip_by_id(db, clip_id)
    if not clip:
        return None
    return {
        "id": clip.id,
        "text": clip.text,
        "summary": clip.summary,
        "date": clip.date
    }

# --- Journals ---
def get_all_journals_service(db: Session, limit: Optional[int] = None):
    return crud.get_all_journals(db, limit)

def get_journal_details_service(db: Session, journal_id: int):
    journal = crud.get_journal_by_id(db, journal_id)
    if not journal:
        return None
    return {
        "id": journal.id,
        "text": journal.text,
        "summary": journal.summary,
        "date": journal.date,
        "theme": journal.theme,
        "strength": journal.strength,
        "growth_area": journal.growth_area
    }

# --- Action Items ---
def get_all_action_items_service(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    return crud.get_all_action_items_with_status(db, include_archived, limit)

def get_action_item_details_service(db: Session, action_item_id: int):
    return crud.get_action_item_by_id(db, action_item_id)

# --- Blockers ---
def get_all_blockers_service(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    return crud.get_all_blockers_with_status(db, include_archived, limit)

def get_blocker_details_service(db: Session, blocker_id: int):
    return crud.get_blocker_by_id(db, blocker_id)

# --- Decisions ---
def get_all_decisions_service(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    return crud.get_all_decisions_with_status(db, include_archived, limit)

def get_decision_details_service(db: Session, decision_id: int):
    return crud.get_decision_by_id(db, decision_id)

# --- Reports ---
def get_weekly_report_service(date: str, force_regen: bool, db):
    """Generate or fetch a weekly report for the week containing the given date."""
    from api.services.process_service import generate_weekly_report
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        report = generate_weekly_report(date_obj, db, force_regen=force_regen)
        if not report:
            return {"error": "No report found or generated for the given week."}
        return {
            "week_start": report.week_start.strftime("%Y-%m-%d"),
            "week_end": report.week_end.strftime("%Y-%m-%d"),
            "summary": report.summary,
            "created_at": report.created_at
        }
    except Exception as e:
        return {"error": str(e)}
    
def list_weekly_reports_service(db):
    from db.crud import list_weekly_reports
    reports = list_weekly_reports(db)
    return [
        {
            "week_start": r.week_start.strftime("%Y-%m-%d"),
            "week_end": r.week_end.strftime("%Y-%m-%d"),
            "created_at": r.created_at,
            "summary": r.summary
        }
        for r in reports
    ]
