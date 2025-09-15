# utils/api_client.py
import requests
import json
BASE_URL = "http://localhost:8000"  # Change if deployed elsewhere

# -------------------- Meetings --------------------
def get_meetings():
    try:
        response = requests.get(f"{BASE_URL}/meeting")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching meetings: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def get_meeting_details(meeting_id):
    try:
        response = requests.get(f"{BASE_URL}/meeting/{meeting_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching meeting details: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

def extract_meeting(transcript):
    try:
        response = requests.post(f"{BASE_URL}/meeting/extract", json={"transcript": transcript})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error extracting meeting: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

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

def extract_clip(text):
    try:
        response = requests.post(f"{BASE_URL}/clip/extract", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error extracting clip: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

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

def extract_journal(text):
    try:
        response = requests.post(f"{BASE_URL}/journal/extract", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error extracting journal: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

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