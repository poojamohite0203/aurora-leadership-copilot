from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.api.services.process_service import extract_and_create_clip

router = APIRouter(prefix="/clips", tags=["clips"])

class ClipInput(BaseModel):
    text: str

@router.post("/extract")
def extract_clip(input: ClipInput):
    """
    Extract structured clip info from text,
    save to DB, and return full clip data.
    """
    try:
        clip_info = extract_and_create_clip(input.text)
        return clip_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))