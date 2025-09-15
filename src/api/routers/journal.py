from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.api.services.process_service import extract_and_create_journal

router = APIRouter(prefix="/journals", tags=["journals"])

class JournalInput(BaseModel):
    text: str

@router.post("/extract")
def extract_journal(input: JournalInput):
    """
    Extract structured journal info from text,
    save to DB, and return full journal data.
    """
    try:
        journal_info = extract_and_create_journal(input.text)
        return journal_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))