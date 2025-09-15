# utils/api_client.py
import requests

BASE_URL = "http://localhost:8000"  # Change if deployed elsewhere

# -------------------- Meetings --------------------
def get_meetings():
    resp = requests.get(f"{BASE_URL}/meeting")
    if resp.status_code == 200:
        return resp.json()
    return []

def get_meeting_details(meeting_id: int):
    resp = requests.get(f"{BASE_URL}/meeting/{meeting_id}")
    if resp.status_code == 200:
        return resp.json()
    return {}

# -------------------- Clips --------------------
def get_clips():
    resp = requests.get(f"{BASE_URL}/clip")
    if resp.status_code == 200:
        return resp.json()
    return []

def get_clip_details(clip_id: int):
    resp = requests.get(f"{BASE_URL}/clip/{clip_id}")
    if resp.status_code == 200:
        return resp.json()
    return {}

# -------------------- Journals --------------------
def get_journals():
    resp = requests.get(f"{BASE_URL}/journal")
    if resp.status_code == 200:
        return resp.json()
    return []

def get_journal_details(journal_id: int):
    resp = requests.get(f"{BASE_URL}/journal/{journal_id}")
    if resp.status_code == 200:
        return resp.json()
    return {}

# -------------------- Action Items --------------------
def get_action_items():
    resp = requests.get(f"{BASE_URL}/action_item")
    if resp.status_code == 200:
        return resp.json()
    return []

# -------------------- Decisions --------------------
def get_decisions():
    resp = requests.get(f"{BASE_URL}/decision")
    if resp.status_code == 200:
        return resp.json()
    return []

# -------------------- Blockers --------------------
def get_blockers():
    resp = requests.get(f"{BASE_URL}/blocker")
    if resp.status_code == 200:
        return resp.json()
    return []

# -------------------- Weekly Reports --------------------
def get_weekly_reports():
    resp = requests.get(f"{BASE_URL}/weekly_report")
    if resp.status_code == 200:
        return resp.json()
    return []

# -------------------- Search & Ask --------------------
def search_items(query: str):
    resp = requests.get(f"{BASE_URL}/search", params={"query": query})
    if resp.status_code == 200:
        return resp.json()
    return []

def ask_ai(query: str):
    resp = requests.post(f"{BASE_URL}/ask", json={"query": query})
    if resp.status_code == 200:
        return resp.json()
    return {"answer": "", "contexts": []}