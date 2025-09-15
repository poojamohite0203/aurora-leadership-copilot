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
