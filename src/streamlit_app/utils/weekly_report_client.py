import requests
from .api_client import BASE_URL

def generate_weekly_report(date_str):
    """Call backend to generate a weekly report for the week containing the given date (YYYY-MM-DD)."""
    try:
        resp = requests.post(f"{BASE_URL}/weekly_report", json={"date": date_str})
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error generating weekly report: {e}")
        return {"error": str(e)}
