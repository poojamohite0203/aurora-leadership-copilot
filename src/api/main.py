from fastapi import FastAPI
from api.routers import meetings

app = FastAPI(title="Aurora AI Leadership Copilot", version="0.1")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])