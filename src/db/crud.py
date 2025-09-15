from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from core import prompt_templates
from db import models

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


def get_all_meetings(db: Session, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """Get all meetings with optional date filtering"""
    query = db.query(models.Meeting)
    
    if from_date:
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        query = query.filter(models.Meeting.date >= from_datetime)
    
    if to_date:
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        query = query.filter(models.Meeting.date <= to_datetime)
    
    return query.all()


def get_meeting_by_id(db: Session, meeting_id: int):
    """Get a specific meeting by ID"""
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()


def get_all_clips(db: Session, limit: Optional[int] = None):
    """Get all clips with optional limit"""
    query = db.query(models.Clip).order_by(models.Clip.date.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_clip_by_id(db: Session, clip_id: int):
    """Get a specific clip by ID"""
    return db.query(models.Clip).filter(models.Clip.id == clip_id).first()


def get_all_journals(db: Session, limit: Optional[int] = None):
    """Get all journals with optional limit"""
    query = db.query(models.Journal).order_by(models.Journal.date.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_journal_by_id(db: Session, journal_id: int):
    """Get a specific journal by ID"""
    return db.query(models.Journal).filter(models.Journal.id == journal_id).first()


def get_all_action_items(db: Session, limit: Optional[int] = None):
    """Get all action items with optional limit"""
    query = db.query(models.Action_Item).order_by(models.Action_Item.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_action_item_by_id(db: Session, action_item_id: int):
    """Get a specific action item by ID"""
    return db.query(models.Action_Item).filter(models.Action_Item.id == action_item_id).first()


def get_all_decisions(db: Session, limit: Optional[int] = None):
    """Get all decisions with optional limit"""
    query = db.query(models.Decision).order_by(models.Decision.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_decision_by_id(db: Session, decision_id: int):
    """Get a specific decision by ID"""
    return db.query(models.Decision).filter(models.Decision.id == decision_id).first()


def get_all_blockers(db: Session, limit: Optional[int] = None):
    """Get all blockers with optional limit"""
    query = db.query(models.Blocker).order_by(models.Blocker.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_blocker_by_id(db: Session, blocker_id: int):
    """Get a specific blocker by ID"""
    return db.query(models.Blocker).filter(models.Blocker.id == blocker_id).first()
