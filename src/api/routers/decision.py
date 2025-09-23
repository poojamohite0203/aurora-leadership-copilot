from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud, models
from db.database import get_db
from typing import Optional
from pydantic import BaseModel
from api.services.get_service import get_all_decisions_service, get_decision_details_service

router = APIRouter(tags=["Decisions"])

class StatusUpdateRequest(BaseModel):
    status: str

@router.get("")
def get_all_decisions(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of decisions returned"),
    include_archived: bool = Query(False, description="Include decided/cancelled decisions")
):
    """
    Return decisions with status filtering.
    By default shows only open decisions.
    """
    try:
        return get_all_decisions_service(db, include_archived, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_decision_details(id: int, db: Session = Depends(get_db)):
    """Get a specific decision by ID"""
    decision = get_decision_details_service(db, id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return decision

@router.put("/{id}/status")
def update_decision_status(
    id: int, 
    request: StatusUpdateRequest, 
    db: Session = Depends(get_db)
):
    """Update decision status"""
    try:
        # Validate status
        status = models.DecisionStatus(request.status)
        
        decision = crud.update_decision_status(db, id, status)
        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        return {"message": f"Decision status updated to {status.value}", "decision": decision}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid options: {[s.value for s in models.DecisionStatus]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
