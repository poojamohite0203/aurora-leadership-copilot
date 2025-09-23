from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from db.database import get_db
from api.services.get_service import get_weekly_report_service,list_weekly_reports_service
from api.services.process_service import post_weekly_report_service
from datetime import datetime

router = APIRouter(tags=["Weekly Report"])

@router.get("/weekly_report")
def get_weekly_report_api(date: str = Query(..., description="Any date in the week to generate report for (YYYY-MM-DD)"), force_regen: bool = False, db: Session = Depends(get_db)):
    """Generate or fetch a weekly report for the week containing the given date."""
    return get_weekly_report_service(date, force_regen, db)

@router.get("/weekly_report/list")
def list_weekly_reports_api(db: Session = Depends(get_db)):
    """List all generated weekly reports."""
    return list_weekly_reports_service(db)

@router.post("/weekly_report")
def post_weekly_report(
    payload: dict = Body(..., example={"date": "2025-09-19", "force_regen": False}),
    db: Session = Depends(get_db)
):
    """Generate or fetch a weekly report for the week containing the given date (POST)."""
    return post_weekly_report_service(payload, db)
