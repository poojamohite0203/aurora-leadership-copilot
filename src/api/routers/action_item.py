from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud
from db.database import get_db
from typing import Optional

router = APIRouter(tags=["Action Items"])

@router.get("")
def get_all_action_items(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of action items returned")
):
    """
    Return all action items.
    Optional limit parameter to control the number of results.
    """
    try:
        return crud.get_all_action_items(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_action_item_details(id: int, db: Session = Depends(get_db)):
    """Get a specific action item by ID"""
    action_item = crud.get_action_item_by_id(db, id)
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return action_item
