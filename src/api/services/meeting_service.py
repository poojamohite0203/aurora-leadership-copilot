from datetime import date
from db.models import Meeting, ActionItem, Decision, Blocker
from core.llm_utils import query_ollama
from core.prompt_templates import MEETING_EXTRACTION_PROMPT
from db.session import SessionLocal

def extract_and_create_meeting(transcript: str):
    """
    Extracts meeting info from transcript using LLM,
    saves all items to DB, and returns full structured data.
    """
    prompt = MEETING_EXTRACTION_PROMPT.format(transcript=transcript)
    llm_response = query_ollama(prompt)  # Expect JSON dict

    meeting_data = llm_response
    db = SessionLocal()

    # 1️⃣ Create Meeting row
    meeting = Meeting(
        title=meeting_data.get("title", "Untitled Meeting"),
        date=date.today(),
        participants=", ".join(meeting_data.get("participants", [])),
        summary=meeting_data.get("summary", "")
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    # 2️⃣ Create related items
    action_items_list, decisions_list, blockers_list = [], [], []

    for action in meeting_data.get("action_items", []):
        db_action = ActionItem(
            meeting_id=meeting.id,
            description=action["description"],
            due_date=action.get("due_date"),
            personal=False,  # personal flag decided in code
            source="meeting",
            source_id=meeting.id
        )
        db.add(db_action)
        db.commit()
        db.refresh(db_action)
        action_items_list.append({
            "id": db_action.id,
            "description": db_action.description,
            "due_date": db_action.due_date,
            "personal": db_action.personal
        })

    for decision in meeting_data.get("decisions", []):
        db_decision = Decision(
            meeting_id=meeting.id,
            description=decision["description"],
            other_options=decision.get("other_options", []),
            personal=False,
            source="meeting",
            source_id=meeting.id
        )
        db.add(db_decision)
        db.commit()
        db.refresh(db_decision)
        decisions_list.append({
            "id": db_decision.id,
            "description": db_decision.description,
            "other_options": db_decision.other_options,
            "personal": db_decision.personal
        })

    for blocker in meeting_data.get("blockers", []):
        db_blocker = Blocker(
            meeting_id=meeting.id,
            description=blocker["description"],
            personal=False,
            source="meeting",
            source_id=meeting.id
        )
        db.add(db_blocker)
        db.commit()
        db.refresh(db_blocker)
        blockers_list.append({
            "id": db_blocker.id,
            "description": db_blocker.description,
            "personal": db_blocker.personal
        })

    # 3️⃣ Return full structured response
    response = {
        "id": meeting.id,
        "title": meeting.title,
        "date_created": str(meeting.date),
        "participants": meeting_data.get("participants", []),
        "summary": meeting.summary,
        "action_items": action_items_list,
        "decisions": decisions_list,
        "blockers": blockers_list
    }

    return response
