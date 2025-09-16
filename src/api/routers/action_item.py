from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud, models
from db.database import get_db
from typing import Optional
from pydantic import BaseModel

router = APIRouter(tags=["Action Items"])

class StatusUpdateRequest(BaseModel):
    status: str

@router.get("")
def get_all_action_items(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of action items returned"),
    include_archived: bool = Query(False, description="Include done/ignored items")
):
    """
    Return action items with status filtering.
    By default shows only open/in_progress items.
    """
    try:
        return crud.get_all_action_items_with_status(db, include_archived, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_action_item_details(id: int, db: Session = Depends(get_db)):
    """Get a specific action item by ID"""
    action_item = crud.get_action_item_by_id(db, id)
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return action_item

@router.put("/{id}/status")
def update_action_item_status(
    id: int, 
    request: StatusUpdateRequest, 
    db: Session = Depends(get_db)
):
    """Update action item status"""
    try:
        # Validate status
        status = models.ActionItemStatus(request.status)
        
        action_item = crud.update_action_item_status(db, id, status)
        if not action_item:
            raise HTTPException(status_code=404, detail="Action item not found")
        
        return {"message": f"Action item status updated to {status.value}", "action_item": action_item}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid options: {[s.value for s in models.ActionItemStatus]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
