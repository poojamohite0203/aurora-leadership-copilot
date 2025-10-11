from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import get_db

from core import models, crud, database, prompt_templates
from core.llm_utils import extract_insights_from_text

router = APIRouter()

@router.post("/extract/meeting")
def extract_and_create_meeting(transcript: str, db: Session = next(get_db())):
    """
    Extract structured data from meeting transcript using LLM.
    Saves Meeting, ActionItems, Decisions, Blockers into DB.
    Returns the full Meeting object with extracted fields.
    """
    # Call generalized LLM method
    extracted = extract_insights_from_text(
        text=transcript,
        prompt_template=prompt_templates.MEETING_EXTRACTION_PROMPT
    )

    if "raw_output" in extracted:
        raise HTTPException(status_code=500, detail="LLM extraction failed")

    # Create Meeting
    meeting = models.Meeting(
        title=extracted.get("title", "Untitled Meeting"),
        date=datetime.utcnow(),
        participants=extracted.get("participants", []),
        summary=extracted.get("summary", "")
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    # Create Action Items
    for item in extracted.get("action_items", []):
        action = models.Action_Item(
            meeting_id=meeting.id,
            description=item.get("description", ""),
            due_date=item.get("due_date"),
            personal=False  # determined by source type
        )
        db.add(action)

    # Create Decisions
    for item in extracted.get("decisions", []):
        decision = models.Decision(
            meeting_id=meeting.id,
            description=item.get("description", ""),
            other_options=item.get("other_options", []),
            personal=False
        )
        db.add(decision)

    # Create Blockers
    for item in extracted.get("blockers", []):
        blocker = models.Blocker(
            meeting_id=meeting.id,
            description=item.get("description", ""),
            personal=False
        )
        db.add(blocker)

    db.commit()

    # Prepare API response with meeting + all related info
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


@router.post("/extract/clip")
def extract_and_create_clip(text: str, db: Session = next(get_db())):
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

    # Extract ActionItems, Decisions, Blockers
    for item in extracted.get("action_items", []):
        db.add(models.Action_Item(
            source="clip",
            source_id=clip.id,
            description=item.get("description", ""),
            due_date=item.get("due_date"),
            personal=False
        ))

    for item in extracted.get("decisions", []):
        db.add(models.Decision(
            source="clip",
            source_id=clip.id,
            description=item.get("description", ""),
            other_options=item.get("other_options", []),
            personal=False
        ))

    for item in extracted.get("blockers", []):
        db.add(models.Blocker(
            source="clip",
            source_id=clip.id,
            description=item.get("description", ""),
            personal=False
        ))

    db.commit()
    return {
        "id": clip.id,
        "text": clip.text,
        "summary": clip.summary,
        "date": clip.date
    }


@router.post("/extract/journal")
def extract_and_create_journal(text: str, db: Session = next(get_db())):
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

    # Extract personal ActionItems, Decisions, Blockers
    for item in extracted.get("action_items", []):
        db.add(models.Action_Item(
            source="journal",
            source_id=journal.id,
            description=item.get("description", ""),
            due_date=item.get("due_date"),
            personal=True
        ))

    for item in extracted.get("decisions", []):
        db.add(models.Decision(
            source="journal",
            source_id=journal.id,
            description=item.get("description", ""),
            other_options=item.get("other_options", []),
            personal=True
        ))

    for item in extracted.get("blockers", []):
        db.add(models.Blocker(
            source="journal",
            source_id=journal.id,
            description=item.get("description", ""),
            personal=True
        ))

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
