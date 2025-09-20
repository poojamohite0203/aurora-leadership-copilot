from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from core import prompt_templates
from db import models
from core import extract_insights_from_text
from db.crud import create_action_items, create_decisions, create_blockers, get_weekly_report, create_weekly_report, list_weekly_reports
from db.vector_store import add_to_index
from sqlalchemy import and_
from core.prompt_templates import WEEKLY_REPORT_PROMPT

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
        participants=extracted.get("participants", []),
        summary=extracted.get("summary", "")
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    create_action_items(db, extracted.get("action_items", []), source="meeting", source_id=None, meeting_id=meeting.id)
    create_decisions(db, extracted.get("decisions", []), source="meeting", source_id=None, meeting_id=meeting.id)
    create_blockers(db, extracted.get("blockers", []), source="meeting", source_id=None, meeting_id=meeting.id)

    db.commit()

    db.refresh(meeting)

    #Index in Chroma (id must be string)
    add_to_index(
    id=f"meeting_{meeting.id}",
    text=transcript,
    metadata={"type": "meeting", "meeting_id": meeting.id})

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

    #Index in Chroma (id must be string)
    add_to_index(
        id=f"clip_{clip.id}",
        text=clip.text,
        metadata={"type": "clip", "clip_id": clip.id}
    )
    
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

    #Index in Chroma (id must be string)
    add_to_index(
    id=f"journal_{journal.id}",
    text=journal.text,
    metadata={"type": "journal", "journal_id": journal.id})

    return {
        "id": journal.id,
        "text": journal.text,
        "summary": journal.summary,
        "date": journal.date,
        "theme": journal.theme,
        "strength": journal.strength,
        "growth_area": journal.growth_area
    }

def get_week_range(date):
    # Always return Monday-Sunday for the week containing 'date'
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def generate_weekly_report(date, db: Session, force_regen=False):
    week_start, week_end = get_week_range(date)
    if not force_regen:
        report = get_weekly_report(db, week_start, week_end)
        if report:
            return report
    # Fetch all data for the week
    meetings = db.query(models.Meeting).filter(and_(models.Meeting.date >= week_start, models.Meeting.date <= week_end)).all()
    clips = db.query(models.Clip).filter(and_(models.Clip.date >= week_start, models.Clip.date <= week_end)).all()
    journals = db.query(models.Journal).filter(and_(models.Journal.date >= week_start, models.Journal.date <= week_end)).all()
    action_items = db.query(models.Action_Item).filter(and_(models.Action_Item.due_date >= week_start, models.Action_Item.due_date <= week_end)).all()
    decisions = db.query(models.Decision).filter(and_(models.Decision.date >= week_start, models.Decision.date <= week_end)).all()
    blockers = db.query(models.Blocker).filter(and_(models.Blocker.date >= week_start, models.Blocker.date <= week_end)).all()
    
    # Extract insights with error handling
    try:
        # Debug: Check if the prompt formatting is the issue
        try:
            # Convert database objects to readable strings
            meetings_str = "\n".join([f"- {m.title}: {m.summary}" for m in meetings]) if meetings else "No meetings this week"
            clips_str = "\n".join([f"- {c.summary}" for c in clips]) if clips else "No clips this week"
            journals_str = "\n".join([f"- {j.summary}" for j in journals]) if journals else "No journals this week"
            action_items_str = "\n".join([f"- {ai.description} (Due: {ai.due_date})" for ai in action_items]) if action_items else "No action items this week"
            decisions_str = "\n".join([f"- {d.description}" for d in decisions]) if decisions else "No decisions this week"
            blockers_str = "\n".join([f"- {b.description}" for b in blockers]) if blockers else "No blockers this week"
            
            formatted_prompt = prompt_templates.WEEKLY_REPORT_PROMPT.format(
                meetings=meetings_str,
                clips=clips_str,
                journals=journals_str,
                action_items=action_items_str,
                decisions=decisions_str,
                blockers=blockers_str,
                week_start=week_start.strftime('%Y-%m-%d'),
                week_end=week_end.strftime('%Y-%m-%d')
            )
        except Exception as prompt_error:
            raise Exception(f"Error formatting prompt: {str(prompt_error)}")
        
        # Debug: Check if LLM processing is the issue
        try:
            # For weekly reports, we already have the formatted prompt, so we need to call the LLM directly
            from core.llm_utils import query_ollama
            import json
            import re
            
            llm_response_text = query_ollama(formatted_prompt)
            
            # Parse the response like extract_insights_from_text does
            try:
                # First try fenced ```json blocks
                match = re.search(r"```json\n(.*)\n```", llm_response_text, re.DOTALL)
                if match:
                    json_string = match.group(1)
                    llm_response = json.loads(json_string)
                else:
                    # Fallback: try any {} JSON block
                    match = re.search(r"\{.*\}", llm_response_text, re.DOTALL)
                    if match:
                        llm_response = json.loads(match.group(0))
                    else:
                        # If no JSON, treat as raw output
                        llm_response = {"raw_output": llm_response_text}
            except json.JSONDecodeError:
                llm_response = {"raw_output": llm_response_text}
                
        except Exception as llm_error:
            raise Exception(f"Error in LLM processing: {str(llm_error)}")
        
        # Check if LLM response is valid
        if "raw_output" in llm_response:
            summary = f"Weekly report for {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}:\n\nNo structured data available for this week."
        else:
            summary = llm_response.get("summary", f"Weekly report for {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}:\n\nSummary not available.")
        
        # Debug: Check if database creation is the issue
        try:
            report = create_weekly_report(db, week_start, week_end, summary)
        except Exception as db_error:
            raise Exception(f"Error creating report in database: {str(db_error)}")
            
        if not report:
            raise Exception("Failed to create weekly report in database - report is None")
        return report
    except Exception as e:
        # Create a basic report if everything fails
        summary = f"Weekly report for {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}:\n\nError generating report: {str(e)}"
        try:
            report = create_weekly_report(db, week_start, week_end, summary)
            return report if report else None
        except:
            return None