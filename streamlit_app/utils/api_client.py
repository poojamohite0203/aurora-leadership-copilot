import requests
import json
import requests
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
        response = requests.post(
            f"{BASE_URL}/meeting/extract", 
            data=transcript,
            headers={"Content-Type": "text/plain"}
        )
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
        response = requests.post(
            f"{BASE_URL}/clip/extract",
            data=text,
            headers={"Content-Type": "text/plain"}
        )
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
        response = requests.post(
            f"{BASE_URL}/journal/extract",
            data=text,
            headers={"Content-Type": "text/plain"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error extracting journal: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

# -------------------- Action Items --------------------
def get_action_items(include_archived: bool = False):
    params = {"include_archived": include_archived}
    resp = requests.get(f"{BASE_URL}/action_item", params=params)
    if resp.status_code == 200:
        return resp.json()
    return []

def update_action_item_status(action_item_id: int, status: str):
    resp = requests.put(f"{BASE_URL}/action_item/{action_item_id}/status", json={"status": status})
    if resp.status_code == 200:
        return resp.json()
    return None

# -------------------- Decisions --------------------
def get_decisions(include_archived: bool = False):
    params = {"include_archived": include_archived}
    resp = requests.get(f"{BASE_URL}/decision", params=params)
    if resp.status_code == 200:
        return resp.json()
    return []

def update_decision_status(decision_id: int, status: str):
    resp = requests.put(f"{BASE_URL}/decision/{decision_id}/status", json={"status": status})
    if resp.status_code == 200:
        return resp.json()
    return None

# -------------------- Blockers --------------------
def get_blockers(include_archived: bool = False):
    params = {"include_archived": include_archived}
    resp = requests.get(f"{BASE_URL}/blocker", params=params)
    if resp.status_code == 200:
        return resp.json()
    return []

def update_blocker_status(blocker_id: int, status: str):
    resp = requests.put(f"{BASE_URL}/blocker/{blocker_id}/status", json={"status": status})
    if resp.status_code == 200:
        return resp.json()
    return None

# -------------------- Weekly Reports --------------------
def get_weekly_reports():
    resp = requests.get(f"{BASE_URL}/weekly_report/list")
    if resp.status_code == 200:
        return resp.json()
    return []

def generate_weekly_report(date_str, force_regen: bool = False):
    """Call backend to generate a weekly report for the week containing the given date (YYYY-MM-DD)."""
    try:
        resp = requests.post(f"{BASE_URL}/weekly_report", json={"date": date_str, "force_regen": force_regen})
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error generating weekly report: {e}")
        return {"error": str(e)}


# -------------------- Search & Ask --------------------
def search_items(query: str):
    resp = requests.get(f"{BASE_URL}/search", params={"query": query})
    if resp.status_code == 200:
        return resp.json()
    return []

def ask_ai(query: str):
    resp = requests.get(f"{BASE_URL}/ask", params={"query": query})
    if resp.status_code == 200:
        return resp.json()
    return {"answer": "", "contexts": []}