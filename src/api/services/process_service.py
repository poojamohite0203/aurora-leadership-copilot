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
import json, re
from core.llm_utils import validate_llm_summary_output, check_moderation, query_gpt

def extract_and_create_meeting(transcript: str, db: Session):
    """
    Extract structured data from meeting transcript using LLM.
    Saves Meeting, ActionItems, Decisions, Blockers into DB.
    Returns the full Meeting object with extracted fields.
    """

    # Moderate Input
    ok, categories = check_moderation(transcript)
    if not ok:
        print(f"User input blocked due to: {categories}")
        raise ValueError(f"User input blocked due to: {categories}")
    
    extracted = extract_insights_from_text(
        text=transcript,
        prompt_template=prompt_templates.MEETING_EXTRACTION_PROMPT
    )
    
    try:
        summary = validate_llm_summary_output(extracted, ["summary"], context="meeting summary")
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    meeting = models.Meeting(
        title=extracted.get("title", "Untitled Meeting"),
        date=datetime.utcnow(),
        participants=extracted.get("participants", []),
        summary=summary
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
    # Moderate Input
    ok, categories = check_moderation(text)
    if not ok:
        print(f"User input blocked due to: {categories}")
        raise ValueError(f"User input blocked due to: {categories}")
    
    extracted = extract_insights_from_text(
        text=text,
        prompt_template=prompt_templates.CLIP_EXTRACTION_PROMPT
    )
    try:
        summary = validate_llm_summary_output(extracted, ["summary"], context="clip summary")
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    clip = models.Clip(
        text=text,
        summary=summary,
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
    # Moderate Input
    ok, categories = check_moderation(text)
    if not ok:
        print(f"User input blocked due to: {categories}")
        raise ValueError(f"User input blocked due to: {categories}")
    
    extracted = extract_insights_from_text(
        text=text,
        prompt_template=prompt_templates.JOURNAL_EXTRACTION_PROMPT
    )
    try:
        summary = validate_llm_summary_output(extracted, ["summary"], context="journal summary")
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    journal = models.Journal(
        text=text,
        summary=summary,
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
    # Always return Monday 00:00:00 to Sunday 23:59:59.999999 for the week containing 'date'
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=7) - timedelta(microseconds=1)
    return week_start, week_end

def generate_weekly_report(date, db: Session, force_regen=False):
    week_start, week_end = get_week_range(date)

    if not force_regen:
        report = get_weekly_report(db, week_start, week_end)
        if report:
            return report

    # 1. Gather weekly data
    # print(f"WEEK RANGE: {week_start} to {week_end}")
    # print("Meeting dates:", [m.date for m in db.query(models.Meeting).all()])
    # print("Clip dates:", [c.date for c in db.query(models.Clip).all()])
    # print("Journal dates:", [j.date for j in db.query(models.Journal).all()])
    # print("Action item dates:", [ai.date for ai in db.query(models.Action_Item).all()])
    # print("Decision dates:", [d.date for d in db.query(models.Decision).all()])
    # print("Blocker dates:", [b.date for b in db.query(models.Blocker).all()])
    
    meetings_str = "\n".join([f"- {m.title}: {m.summary}" for m in db.query(models.Meeting).filter(
        models.Meeting.date.between(week_start, week_end))]) or "No meetings this week"
    
    clips_str = "\n".join([f"- {c.text}" for c in db.query(models.Clip).filter(
        models.Clip.date.between(week_start, week_end))]) or "No clips this week"
    
    journals_str = "\n".join([f"- {j.text}" for j in db.query(models.Journal).filter(
        models.Journal.date.between(week_start, week_end))]) or "No journals this week"
    
    action_items_str = "\n".join([f"- {ai.description} (Due: {ai.due_date})"
        for ai in db.query(models.Action_Item).filter(
            models.Action_Item.date.between(week_start, week_end))]) or "No action items this week"
    
    decisions_str = "\n".join([f"- {d.description}" for d in db.query(models.Decision).filter(
        models.Decision.date.between(week_start, week_end))]) or "No decisions this week"
    
    blockers_str = "\n".join([f"- {b.description}" for b in db.query(models.Blocker).filter(
        models.Blocker.date.between(week_start, week_end))]) or "No blockers this week"

    # 2. Build prompt
    formatted_prompt = prompt_templates.WEEKLY_REPORT_PROMPT.format(
        week_start=week_start.strftime('%Y-%m-%d'),
        week_end=week_end.strftime('%Y-%m-%d'),
        meetings=meetings_str,
        clips=clips_str,
        journals=journals_str,
        action_items=action_items_str,
        decisions=decisions_str,
        blockers=blockers_str,
    )
    #print("Formatted Prompt: ", formatted_prompt)

    # 3. Query LLM
    llm_response_text = query_gpt(formatted_prompt)
    # print("LLM Response Text: ", llm_response_text)
    
    try:
        parsed = extract_summary_from_response(llm_response_text)
        # print("DEBUG: Type of parsed:", type(parsed))
        # print("DEBUG: Parsed content:", parsed)
        
        # More explicit extraction with better error handling
        if isinstance(parsed, dict) and "summary" in parsed:
            summary_text = parsed["summary"]
            # print("DEBUG: Successfully extracted summary from dict")
        else:
            # print("DEBUG: Failed to extract summary from dict, using raw text")
            summary_text = llm_response_text
            
        # print("DEBUG: Type of summary_text:", type(summary_text))
        # print("DEBUG: summary_text content:", repr(summary_text[:200]))
    except Exception as e:
        # print(f"Exception in extract_summary_from_response: {e}")
        summary_text = llm_response_text

    # print("Summary Text: ", summary_text)

    # Use guardrail for weekly summary
    try:
        # print("DEBUG: Before validation - summary_text:", repr(summary_text[:200]))
        validated_summary = validate_llm_summary_output({"summary": summary_text}, ["summary"], context="weekly summary")
        # print("DEBUG: After validation - type:", type(validated_summary))
        # print("DEBUG: After validation - content:", repr(validated_summary[:200]))
        summary_text = validated_summary
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    # print("DEBUG: Final summary_text before DB save:", repr(summary_text[:200]))
    report = create_weekly_report(db, week_start, week_end, summary_text)

    return report

def extract_summary_from_response(response: str) -> dict:
    """
    Extract the summary JSON string safely, escaping control characters if needed.
    Handles non-strict JSON by attempting to extract the summary value with regex if parsing fails.
    """
    from core.llm_utils import extract_json_from_llm_response
    
    # print("DEBUG extract_summary_from_response: Input response:", repr(response[:200]))
    result = extract_json_from_llm_response(response)
    # print("DEBUG extract_summary_from_response: extract_json_from_llm_response result:", result)
    
    # If extraction failed, try to extract summary value directly as fallback
    if "raw_output" in result:
        import re
        match = re.search(r'summary"?\s*:\s*"([^"]+)"', response)
        if match:
            # print("DEBUG extract_summary_from_response: Using regex fallback, extracted:", match.group(1))
            return {"summary": match.group(1)}
        # print("DEBUG extract_summary_from_response: Regex fallback failed")
        return {"summary": "Summary generation failed: Output format invalid or empty."}
    
    # print("DEBUG extract_summary_from_response: Returning result:", result)
    return result

def post_weekly_report_service(payload: dict, db):
    """Generate or fetch a weekly report for the week containing the given date (POST)."""
    from datetime import datetime
    try:
        date_str = payload.get("date")
        force_regen = payload.get("force_regen", False)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
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
