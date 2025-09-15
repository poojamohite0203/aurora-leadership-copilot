from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud
from db.database import get_db
from typing import Optional

router = APIRouter(tags=["Decisions"])

@router.get("")
def get_all_decisions(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of decisions returned")
):
    """
    Return all decisions.
    Optional limit parameter to control the number of results.
    """
    try:
        return crud.get_all_decisions(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_decision_details(id: int, db: Session = Depends(get_db)):
    """Get a specific decision by ID"""
    decision = crud.get_decision_by_id(db, id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return decision
