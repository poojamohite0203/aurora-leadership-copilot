from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from core import prompt_templates
from db import models
from sqlalchemy.orm import joinedload

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
            date=parse_due_date(item.get("due_date")) or datetime.utcnow(),
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
            personal=personal,
            date=datetime.utcnow()
        )
        db.add(decision)


def create_blockers(db: Session, items: list, source: str, source_id: int, meeting_id: Optional[int] = None, personal: bool = False):
    for item in items:
        blocker = models.Blocker(
            meeting_id=meeting_id,
            source=source,
            source_id=source_id,
            description=item.get("description", ""),
            personal=personal,
            date=datetime.utcnow()
        )
        db.add(blocker)


def get_all_meetings(db: Session, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """Get all meetings with optional date filtering"""
    query = db.query(models.Meeting).options(
        joinedload(models.Meeting.action_items),
        joinedload(models.Meeting.decisions),
        joinedload(models.Meeting.blockers)
    )
    
    if from_date:
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        query = query.filter(models.Meeting.date >= from_datetime)
    
    if to_date:
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        query = query.filter(models.Meeting.date <= to_datetime)
    
    return query.all()


def get_meeting_by_id(db: Session, meeting_id: int):
    """Get a specific meeting by ID with related action_items, decisions, and blockers eagerly loaded"""
    return (
        db.query(models.Meeting)
        .options(
            joinedload(models.Meeting.action_items),
            joinedload(models.Meeting.decisions),
            joinedload(models.Meeting.blockers)
        )
        .filter(models.Meeting.id == meeting_id)
        .first()
    )

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


# Status-aware CRUD functions
def get_all_action_items_with_status(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    """Get action items filtered by status"""
    query = db.query(models.Action_Item)
    
    if not include_archived:
        # Only show open and in_progress items by default
        query = query.filter(models.Action_Item.status.in_([models.ActionItemStatus.OPEN, models.ActionItemStatus.IN_PROGRESS]))
    
    query = query.order_by(models.Action_Item.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_all_decisions_with_status(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    """Get decisions filtered by status"""
    query = db.query(models.Decision)
    
    if not include_archived:
        # Only show open items by default
        query = query.filter(models.Decision.status == models.DecisionStatus.OPEN)
    
    query = query.order_by(models.Decision.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def get_all_blockers_with_status(db: Session, include_archived: bool = False, limit: Optional[int] = None):
    """Get blockers filtered by status"""
    query = db.query(models.Blocker)
    
    if not include_archived:
        # Only show open and in_progress items by default
        query = query.filter(models.Blocker.status.in_([models.BlockerStatus.OPEN, models.BlockerStatus.IN_PROGRESS]))
    
    query = query.order_by(models.Blocker.id.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def update_action_item_status(db: Session, action_item_id: int, status: models.ActionItemStatus):
    """Update action item status"""
    action_item = db.query(models.Action_Item).filter(models.Action_Item.id == action_item_id).first()
    if action_item:
        action_item.status = status
        db.commit()
        db.refresh(action_item)
    return action_item


def update_decision_status(db: Session, decision_id: int, status: models.DecisionStatus):
    """Update decision status"""
    decision = db.query(models.Decision).filter(models.Decision.id == decision_id).first()
    if decision:
        decision.status = status
        db.commit()
        db.refresh(decision)
    return decision


def update_blocker_status(db: Session, blocker_id: int, status: models.BlockerStatus):
    """Update blocker status"""
    blocker = db.query(models.Blocker).filter(models.Blocker.id == blocker_id).first()
    if blocker:
        blocker.status = status
        db.commit()
        db.refresh(blocker)
    return blocker


def get_weekly_report(db, week_start, week_end):
    return db.query(models.WeeklyReport).filter_by(week_start=week_start, week_end=week_end).first()

def create_weekly_report(db, week_start, week_end, summary):
    report = models.WeeklyReport(week_start=week_start, week_end=week_end, summary=summary)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def list_weekly_reports(db):
    return db.query(models.WeeklyReport).order_by(models.WeeklyReport.week_start.desc()).all()
