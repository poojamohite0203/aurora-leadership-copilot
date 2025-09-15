from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud
from db.database import get_db
from typing import Optional

router = APIRouter(tags=["Blockers"])

@router.get("")
def get_all_blockers(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of blockers returned")
):
    """
    Return all blockers.
    Optional limit parameter to control the number of results.
    """
    try:
        return crud.get_all_blockers(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_blocker_details(id: int, db: Session = Depends(get_db)):
    """Get a specific blocker by ID"""
    blocker = crud.get_blocker_by_id(db, id)
    if not blocker:
        raise HTTPException(status_code=404, detail="Blocker not found")
    
    return blocker
