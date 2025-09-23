from sqlalchemy.orm import Session
from db import crud, models

def update_action_item_status_service(db: Session, action_item_id: int, status_str: str):
    """Update action item status and return updated item or error info."""
    try:
        # Validate status
        status = models.ActionItemStatus(status_str)
        action_item = crud.update_action_item_status(db, action_item_id, status)
        if not action_item:
            return None, f"Action item {action_item_id} not found"
        return action_item, None
    except ValueError:
        valid_statuses = [s.value for s in models.ActionItemStatus]
        return None, f"Invalid status. Valid options: {valid_statuses}"
    except Exception as e:
        return None, str(e)
