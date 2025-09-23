try:
    # Try imports for Streamlit Cloud (src as package)
    from src.api.services.get_service import (
        get_all_meetings_service, get_meeting_details_service, get_all_clips_service, get_clip_details_service,
        get_all_journals_service, get_journal_details_service, get_all_action_items_service, get_all_decisions_service,
        get_all_blockers_service, list_weekly_reports_service
    )
    from src.api.services.process_service import (
        extract_and_create_meeting, extract_and_create_clip, extract_and_create_journal, post_weekly_report_service
    )
    from src.api.services.search_service import search_items_service
    from src.api.services.update_service import update_action_item_status_service
    from src.db.database import SessionLocal
    from src.db import crud
except ImportError:
    # Fallback to absolute imports (for local development)
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
    
    from api.services.get_service import (
        get_all_meetings_service, get_meeting_details_service, get_all_clips_service, get_clip_details_service,
        get_all_journals_service, get_journal_details_service, get_all_action_items_service, get_all_decisions_service,
        get_all_blockers_service, list_weekly_reports_service
    )
    from api.services.process_service import (
        extract_and_create_meeting, extract_and_create_clip, extract_and_create_journal, post_weekly_report_service
    )
    from api.services.search_service import search_items_service
    from api.services.update_service import update_action_item_status_service

def get_db_session():
    """Create database session"""
    try:
        from src.db.database import SessionLocal
        return SessionLocal()
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
        from db.database import SessionLocal
        return SessionLocal()

def get_crud():
    """Get CRUD operations"""
    try:
        from src.db import crud
        return crud
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
        from db import crud
        return crud

# -------------------- Meetings --------------------
def get_meetings():
    with get_db_session() as db:
        return get_all_meetings_service(db)

def get_meeting_details(meeting_id):
    with get_db_session() as db:
        return get_meeting_details_service(db, meeting_id)

def extract_meeting(transcript):
    with get_db_session() as db:
        return extract_and_create_meeting(transcript, db)

# -------------------- Clips --------------------
def get_clips():
    with get_db_session() as db:
        return get_all_clips_service(db)

def get_clip_details(clip_id: int):
    with get_db_session() as db:
        return get_clip_details_service(db, clip_id)

def extract_clip(text):
    with get_db_session() as db:
        return extract_and_create_clip(text, db)

# -------------------- Journals --------------------
def get_journals():
    with get_db_session() as db:
        return get_all_journals_service(db)

def get_journal_details(journal_id: int):
    with get_db_session() as db:
        return get_journal_details_service(db, journal_id)

def extract_journal(text):
    with get_db_session() as db:
        return extract_and_create_journal(text, db)

# -------------------- Action Items --------------------
def get_action_items(include_archived: bool = False):
    with get_db_session() as db:
        return get_all_action_items_service(db, include_archived)

def update_action_item_status(action_item_id: int, status: str):
    with get_db_session() as db:
        return update_action_item_status_service(db, action_item_id, status)

# -------------------- Decisions --------------------
def get_decisions(include_archived: bool = False):
    with get_db_session() as db:
        return get_all_decisions_service(db, include_archived)

def update_decision_status(decision_id: int, status: str):
    with get_db_session() as db:
        return get_crud().update_decision_status(db, decision_id, status)

# -------------------- Blockers --------------------
def get_blockers(include_archived: bool = False):
    with get_db_session() as db:
        return get_all_blockers_service(db, include_archived)

def update_blocker_status(blocker_id: int, status: str):
    with get_db_session() as db:
        return get_crud().update_blocker_status(db, blocker_id, status)

# -------------------- Weekly Reports --------------------
def get_weekly_reports():
    with get_db_session() as db:
        return list_weekly_reports_service(db)

def generate_weekly_report(date_str, force_regen: bool = False):
    with get_db_session() as db:
        return post_weekly_report_service({"date": date_str, "force_regen": force_regen}, db)

# -------------------- Search & Ask --------------------
def search_items(query: str):
    return search_items_service(query)

def ask_ai(query: str):
    """Ask AI using RAG service - placeholder implementation"""
    # TODO: Implement proper RAG functionality
    return {
        "answer": "RAG functionality needs to be implemented. This is a placeholder response.",
        "context_used": ["Feature in development"]
    }