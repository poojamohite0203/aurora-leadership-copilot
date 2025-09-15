# ui/pages/meetings.py
import streamlit as st
from utils.api_client import get_meetings, get_meeting_details

st.set_page_config(page_title="Meetings", layout="wide")

st.title("📅 Meetings")

# ---- Fetch meetings ----
meetings = get_meetings()

if not meetings:
    st.info("No meetings found yet.")
else:
    # Sidebar filter
    meeting_titles = [f"{m['id']} - {m['title']}" for m in meetings]
    selected = st.sidebar.selectbox("Select a meeting", meeting_titles)

    meeting_id = int(selected.split(" - ")[0])
    details = get_meeting_details(meeting_id)

    # Show summary card
    st.subheader(details["title"])
    st.caption(f"📆 Date: {details.get('date')}")
    st.write(f"**Summary:** {details.get('summary', 'N/A')}")

    # Participants
    if details.get("participants"):
        st.write("👥 **Participants**")
        st.write(", ".join(details["participants"]))

    # Related items (expanders)
    with st.expander("✅ Action Items"):
        if details.get("action_items"):
            for a in details["action_items"]:
                st.write(f"- {a['description']} (due: {a.get('due_date','N/A')})")
        else:
            st.write("No action items.")

    with st.expander("🗳 Decisions"):
        if details.get("decisions"):
