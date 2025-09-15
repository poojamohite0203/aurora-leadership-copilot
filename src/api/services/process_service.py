from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from db.database import get_db
from core import prompt_templates
from db import models
from core import extract_insights_from_text


def parse_due_date(due_date_str):
    """Convert due_date string to datetime object or None"""
    if not due_date_str or due_date_str in ["", "Not specified", "None", None]:
        return None
    
    # If it's already a datetime object, return it
    if isinstance(due_date_str, datetime):
        return due_date_str
    
    # Try to parse common date formats
    try:
        # Try ISO format first
        return datetime.fromisoformat(due_date_str)
    except (ValueError, AttributeError):
        try:
            # Try common date formats
            for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]:
                try:
                    return datetime.strptime(due_date_str, fmt)
                except ValueError:
                    continue
        except:
            pass
    
    # If all parsing fails, return None
    return None


def create_action_items(db: Session, items: list, source: str, source_id: int, meeting_id: Optional[int] = None, personal: bool = False):
    for item in items:
        action_item = models.Action_Item(
            meeting_id=meeting_id,
            source=source,
            source_id=source_id,
            description=item.get("description", ""),
            due_date=parse_due_date(item.get("due_date")),
            personal=personal
        )
        db.add(action_item)


def create_decisions(db: Session, items: list, source: str, source_id: int, meeting_id: Optional[int] = None, personal: bool = False):
    for item in items:
        decision = models.Decision(
            meeting_id=meeting_id,
            source=source,
            source_id=source_id,
            description=item.get("description", ""),
            other_options=item.get("other_options", {}),
            personal=personal
        )
        db.add(decision)


def create_blockers(db: Session, items: list, source: str, source_id: int, meeting_id: Optional[int] = None, personal: bool = False):
    for item in items:
        blocker = models.Blocker(
            meeting_id=meeting_id,
            source=source,
            source_id=source_id,
            description=item.get("description", ""),
            personal=personal
        )
        db.add(blocker)


def extract_and_create_meeting(transcript: str, db: Session):
    """
    Extract structured data from meeting transcript using LLM.
    Saves Meeting, ActionItems, Decisions, Blockers into DB.
    Returns the full Meeting object with extracted fields.
    """
    extracted = extract_insights_from_text(
        text=transcript,
        prompt_template=prompt_templates.MEETING_EXTRACTION_PROMPT
    )

    if "raw_output" in extracted:
        raise HTTPException(status_code=500, detail="LLM extraction failed")

    meeting = models.Meeting(
        title=extracted.get("title", "Untitled Meeting"),
        date=datetime.utcnow(),
        participants=extracted.get("participants", []),  # Keep as list - now stored as JSON
        summary=extracted.get("summary", "")
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    create_action_items(db, extracted.get("action_items", []), source=None, source_id=None, meeting_id=meeting.id)
    create_decisions(db, extracted.get("decisions", []), source=None, source_id=None, meeting_id=meeting.id)
    create_blockers(db, extracted.get("blockers", []), source=None, source_id=None, meeting_id=meeting.id)

    db.commit()

    db.refresh(meeting)
    return {
        "id": meeting.id,
        "title": meeting.title,
        "summary": meeting.summary,
        "date": meeting.date,
        "participants": meeting.participants,
        "action_items": [a.__dict__ for a in db.query(models.Action_Item).filter_by(meeting_id=meeting.id)],
        "decisions": [d.__dict__ for d in db.query(models.Decision).filter_by(meeting_id=meeting.id)],
        "blockers": [b.__dict__ for b in db.query(models.Blocker).filter_by(meeting_id=meeting.id)]
    }


def extract_and_create_clip(text: str, db: Session):
    """
    Extract ActionItems, Decisions, Blockers from a clip or chat text.
    Saves to DB as Clip and related tables.
    """
    extracted = extract_insights_from_text(
        text=text,
        prompt_template=prompt_templates.CLIP_EXTRACTION_PROMPT
    )

    if "raw_output" in extracted:
        raise HTTPException(status_code=500, detail="LLM extraction failed")

    clip = models.Clip(
        text=text,
        summary=extracted.get("summary", ""),
        date=datetime.utcnow()
    )
    db.add(clip)
    db.commit()
    db.refresh(clip)

    create_action_items(db, extracted.get("action_items", []), source="clip", source_id=clip.id)
    create_decisions(db, extracted.get("decisions", []), source="clip", source_id=clip.id)
    create_blockers(db, extracted.get("blockers", []), source="clip", source_id=clip.id)

    db.commit()
    return {
        "id": clip.id,
        "text": clip.text,
        "summary": clip.summary,
        "date": clip.date
    }


def extract_and_create_journal(text: str, db: Session):
    """
    Extract structured insights from personal journal text.
    Saves Journal entry and associated ActionItems, Decisions, Blockers.
    Personal flag is True for all extracted items.
    """
    extracted = extract_insights_from_text(
        text=text,
        prompt_template=prompt_templates.JOURNAL_EXTRACTION_PROMPT
    )

    if "raw_output" in extracted:
        raise HTTPException(status_code=500, detail="LLM extraction failed")

    journal = models.Journal(
        text=text,
        summary=extracted.get("summary", ""),
        date=datetime.utcnow(),
        theme=extracted.get("theme", []),
        strength=extracted.get("strength", []),
        growth_area=extracted.get("growth_area", [])
    )
    db.add(journal)
    db.commit()
    db.refresh(journal)

    create_action_items(db, extracted.get("action_items", []), source="journal", source_id=journal.id, personal=True)
    create_decisions(db, extracted.get("decisions", []), source="journal", source_id=journal.id, personal=True)
    create_blockers(db, extracted.get("blockers", []), source="journal", source_id=journal.id, personal=True)

    db.commit()
    return {
        "id": journal.id,
        "text": journal.text,
        "summary": journal.summary,
        "date": journal.date,
        "theme": journal.theme,
        "strength": journal.strength,
        "growth_area": journal.growth_area
    }