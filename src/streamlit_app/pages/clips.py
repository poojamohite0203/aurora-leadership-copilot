# ui/pages/clips.py
import streamlit as st
from utils.api_client import get_clips, get_clip_details

st.set_page_config(page_title="Clips", layout="wide")
st.title("📋 Clipboard History")

clips = get_clips()

if not clips:
    st.info("No clips found yet.")
else:
    selected = st.sidebar.selectbox("Select a clip", [f"{c['id']} - {c['summary'][:40]}" for c in clips])
    clip_id = int(selected.split(" - ")[0])
    details = get_clip_details(clip_id)

    st.subheader(f"Clip #{clip_id}")
    st.caption(f"📆 Date: {details.get('date')}")
    st.write(f"**Summary:** {details.get('summary', '')}")
    st.write("📝 Full Text")
    st.write(details.get("text", ""))

    with st.expander("✅ Action Items"):
        for a in details.get("action_items", []):
            st.write(f"- {a['description']} (due: {a.get('due_date','N/A')})")

    with st.expander("🗳 Decisions"):
        for d in details.get("decisions", []):
            st.write(f"- {d['description']}")

    with st.expander("⛔ Blockers"):
        for b in details.get("blockers", []):
            st.write(f"- {b['description']}")