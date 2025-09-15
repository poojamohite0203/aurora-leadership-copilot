import streamlit as st
from utils.api_client import get_meetings, get_meeting_details, extract_meeting
from sidebar import render_sidebar

st.set_page_config(page_title="Meetings", layout="wide")

# Render the custom sidebar
render_sidebar()

st.title("📅 Meetings")

# Add new meeting section
st.header("➕ Add New Meeting")
with st.expander("Add Meeting Transcript", expanded=False):
    transcript_text = st.text_area(
        "Enter meeting transcript:",
        placeholder="Paste your raw meeting transcript here (with timestamps, speaker names, etc.). The AI will automatically parse and extract insights.\n\nExample:\n'John Smith 9:30 AM: Let's discuss the API integration...\nJane Doe 9:32 AM: I think we should prioritize security...'",
        height=250,
        key="meeting_transcript"
    )
    
    if st.button("Extract Meeting Data", key="extract_meeting"):
        if transcript_text.strip():
            with st.spinner("Processing meeting transcript..."):
                result = extract_meeting(transcript_text)
                if result:
                    st.success(f"✅ Meeting extracted successfully! Meeting ID: {result.get('id', 'N/A')}")
                    st.rerun()  # Refresh the page to show the new meeting
                else:
                    st.error("❌ Failed to extract meeting data. Please try again.")
        else:
            st.warning("Please enter a meeting transcript.")

st.divider()

# ---- Fetch meetings ----
meetings = get_meetings()
# st.write("Debug - meetings content:", meetings) -- degugger info on  UI
# Safety check: ensure meetings is a list of dicts
if isinstance(meetings, str):
    st.error("API returned a string instead of JSON. Check your api_client.py")
    st.stop()
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
            for d in details["decisions"]:
                st.write(f"- {d['description']}")
        else:
            st.write("No decisions.")

    with st.expander("⛔ Blockers"):
        if details.get("blockers"):
            for b in details["blockers"]:
                st.write(f"- {b['description']}")
        else:
            st.write("No blockers.")