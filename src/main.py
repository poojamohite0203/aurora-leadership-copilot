from fastapi import FastAPI
from api.routers import meeting
from api.routers import clip
from api.routers import journal
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

# create tables 
models.Base.metadata.create_all(bind=engine)