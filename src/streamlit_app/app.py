import streamlit as st
from utils.api_client import get_meetings, get_clips, get_journals, get_action_items
from sidebar import render_sidebar

st.set_page_config(page_title="AI Productivity Dashboard", layout="wide")

# Render the custom sidebar
render_sidebar()

st.title("📊 Productivity Dashboard")

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
    active_actions = [a for a in actions if a.get("status") in ["open", "in_progress"]]
    st.metric("Open Action Items", len(active_actions))
    st.page_link("pages/action_tracker.py", label="Action Tracker")

with col3:
    st.metric("Latest Clips", len(clips))
    if clips:
        st.write(f"📝 {clips[-1]['summary'][:50]}...")
    st.page_link("pages/clips.py", label="View Clips")

with col4:
    if journals:
        st.metric("Latest Journal", len(journals))
        st.write(f"📔 {journals[-1]['text'][:50]}...")
    else:
        st.metric("Latest Journal", 0)
    st.page_link("pages/journals.py", label="View Journals")

# ---- Weekly Report Section ----
st.subheader("📅 Weekly Status Report")
st.write("Generate and review your weekly summary.")
st.page_link("pages/status_report.py", label="Go to Weekly Reports")