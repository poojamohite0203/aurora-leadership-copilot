from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import crud, models
from db.database import get_db
from typing import Optional
from pydantic import BaseModel
from api.services.get_service import get_all_blockers_service, get_blocker_details_service

router = APIRouter(tags=["Blockers"])

class StatusUpdateRequest(BaseModel):
    status: str

@router.get("")
def get_all_blockers(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, description="Limit the number of blockers returned"),
    include_archived: bool = Query(False, description="Include resolved/ignored blockers")
):
    """
    Return blockers with status filtering.
    By default shows only open/in_progress blockers.
    """
    try:
        return get_all_blockers_service(db, include_archived, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_blocker_details(id: int, db: Session = Depends(get_db)):
    """Get a specific blocker by ID"""
    blocker = get_blocker_details_service(db, id)
    if not blocker:
        raise HTTPException(status_code=404, detail="Blocker not found")
    
    return blocker

@router.put("/{id}/status")
def update_blocker_status(
    id: int, 
    request: StatusUpdateRequest, 
    db: Session = Depends(get_db)
):
    """Update blocker status"""
    try:
        # Validate status
        status = models.BlockerStatus(request.status)
        
        blocker = crud.update_blocker_status(db, id, status)
        if not blocker:
            raise HTTPException(status_code=404, detail="Blocker not found")
        
        return {"message": f"Blocker status updated to {status.value}", "blocker": blocker}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid options: {[s.value for s in models.BlockerStatus]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
