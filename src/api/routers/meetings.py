from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.api.services.process_service import extract_and_create_meeting

router = APIRouter(prefix="/meetings", tags=["meetings"])

class TranscriptInput(BaseModel):
    transcript: str

@router.post("/extract")
def extract_meeting(input: TranscriptInput):
    """
    Extract structured meeting info from transcript,
    save to DB, and return full meeting data.
    """
    try:
        meeting_info = extract_and_create_meeting(input.transcript)
        return meeting_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
