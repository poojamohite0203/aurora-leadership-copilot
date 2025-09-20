from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from db.database import get_db
from api.services.process_service import generate_weekly_report, list_weekly_reports
from datetime import datetime

router = APIRouter(tags=["Weekly Report"])

@router.get("/weekly_report")
def get_weekly_report_api(date: str = Query(..., description="Any date in the week to generate report for (YYYY-MM-DD)"), force_regen: bool = False, db: Session = Depends(get_db)):
    """Generate or fetch a weekly report for the week containing the given date."""
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        report = generate_weekly_report(date_obj, db, force_regen=force_regen)
        if not report:
            return {"error": "No report found or generated for the given week."}
        return {
            "week_start": report.week_start.strftime("%Y-%m-%d"),
            "week_end": report.week_end.strftime("%Y-%m-%d"),
            "summary": report.summary,
            "created_at": report.created_at
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/weekly_report/list")
def list_weekly_reports_api(db: Session = Depends(get_db)):
    """List all generated weekly reports."""
    reports = list_weekly_reports(db)
    return [
        {
            "week_start": r.week_start.strftime("%Y-%m-%d"),
            "week_end": r.week_end.strftime("%Y-%m-%d"),
            "created_at": r.created_at,
            "summary": r.summary
        }
        for r in reports
    ]

@router.post("/weekly_report")
def post_weekly_report(
    payload: dict = Body(..., example={"date": "2025-09-19", "force_regen": False}),
    db: Session = Depends(get_db)
):
    """Generate or fetch a weekly report for the week containing the given date (POST)."""
    try:
        date_str = payload.get("date")
        force_regen = payload.get("force_regen", False)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        report = generate_weekly_report(date_obj, db, force_regen=force_regen)
        if not report:
            return {"error": "No report found or generated for the given week."}
        return {
            "week_start": report.week_start.strftime("%Y-%m-%d"),
            "week_end": report.week_end.strftime("%Y-%m-%d"),
            "summary": report.summary,
            "created_at": report.created_at
        }
    except Exception as e:
        return {"error": str(e)}
