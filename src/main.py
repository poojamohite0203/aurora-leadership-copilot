from fastapi import FastAPI
from api.routers import meeting
from api.routers import clip
from api.routers import journal
from api.routers import rag
from api.routers import search
from api.routers import action_item
from api.routers import decision
from api.routers import blocker
from api.routers import weekly_report
from db.database import engine
from db import models

app = FastAPI(title="Aurora AI Leadership Copilot", version="0.1")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(meeting.router, prefix="/meeting", tags=["Meeting"])

app.include_router(clip.router, prefix="/clip", tags=["Clip"])

app.include_router(journal.router, prefix="/journal", tags=["Journal"])

app.include_router(action_item.router, prefix="/action_item", tags=["Action Items"])

app.include_router(decision.router, prefix="/decision", tags=["Decisions"])

app.include_router(blocker.router, prefix="/blocker", tags=["Blockers"])

app.include_router(search.router, prefix="", tags=["Search"])

app.include_router(rag.router, prefix="", tags=["RAG"])

app.include_router(weekly_report.router, prefix="", tags=["Weekly Report"])


# create tables 
models.Base.metadata.create_all(bind=engine)