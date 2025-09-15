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