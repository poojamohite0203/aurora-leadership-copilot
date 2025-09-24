import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

from streamlit_app.utils.backend_client import get_meetings, get_clips, get_journals, get_action_items
from streamlit_app.sidebar import render_sidebar

st.set_page_config(page_title="AI Productivity Dashboard", layout="wide")

# Render the custom sidebar
render_sidebar()

st.title("📊 Productivity Dashboard")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:12px; border-radius:8px; margin-bottom:18px;'>
<b>Welcome to your AI Productivity Dashboard!</b><br>
- <b>Meetings</b>: Track and review all your meetings.<br>
- <b>Action Items</b>: See what needs to be done and update progress.<br>
- <b>Clips</b>: Store and search important notes or snippets.<br>
- <b>Journals</b>: Reflect on your work and capture insights.<br>
- <b>Weekly Status Report</b>: Get an AI-generated summary of your week.<br><br>
<b>How to use:</b><br>
- Click any link to view details and manage your work.<br>
- Use the sidebar to quickly navigate between sections.<br>
</div>
""", unsafe_allow_html=True)

# ---- Fetch data from backend ----
meetings = get_meetings()
clips = get_clips()
journals = get_journals()
actions = get_action_items(include_archived=False)  # Only active items for dashboard

# ---- Summary Cards (4 columns) ----
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("This Week’s Meetings", len(meetings))
    st.page_link("pages/meetings.py", label="View Meetings")

with col2:
    # Only count open and in_progress action items
    active_actions = [a for a in actions if hasattr(a, 'status') and a.status in ["open", "in_progress"]]
    st.metric("Open Action Items", len(active_actions))
    st.page_link("pages/action_tracker.py", label="Action Tracker")

with col3:
    st.metric("Latest Clips", len(clips))
    if clips:
        st.write(f"📝 {clips[-1].summary[:50]}...")
    st.page_link("pages/clips.py", label="View Clips")

with col4:
    if journals:
        st.metric("Latest Journal", len(journals))
        st.write(f"📔 {journals[-1].text[:50]}...")
    else:
        st.metric("Latest Journal", 0)
    st.page_link("pages/journals.py", label="View Journals")

# ---- Weekly Report Section ----
st.subheader("📅 Weekly Status Report")
st.write("Generate and review your weekly summary.")
st.page_link("pages/status_report.py", label="Go to Weekly Reports")