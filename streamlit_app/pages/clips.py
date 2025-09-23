import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import streamlit as st
from utils.api_client import get_clips, get_clip_details, extract_clip
from sidebar import render_sidebar

st.set_page_config(page_title="Clips", layout="wide")
st.title("📋 Clipboard History")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- Add new clips using the form above.<br>
- Select a clip from the sidebar to view details.<br>
- See extracted <b>Summary</b> and <b>Full Text</b> for each clip.<br>
</div>
""", unsafe_allow_html=True)

# Render the custom sidebar 
render_sidebar()

# Add new clip section
st.header("➕ Add New Clip")
with st.expander("Add Text Clip", expanded=False):
    # Initialize or clear the session state if needed
    if "clear_clip_text" in st.session_state and st.session_state["clear_clip_text"]:
        st.session_state["clip_text"] = ""
        st.session_state["clear_clip_text"] = False
        st.rerun()
    
    if "clip_text" not in st.session_state:
        st.session_state["clip_text"] = ""
    
    clip_text = st.text_area(
        "Enter text or note:",
        placeholder="Paste your text, note, or snippet here...",
        height=150,
        key="clip_text"
    )
    
    if st.button("Extract Clip Data", key="extract_clip"):
        if clip_text.strip():
            with st.spinner("Processing text clip..."):
                result = extract_clip(clip_text)
                if result:
                    st.success(f"✅ Clip extracted successfully! Clip ID: {result.get('id', 'N/A')}")
                    st.session_state["clear_clip_text"] = True
                    st.rerun()
                else:
                    st.error("❌ Failed to extract clip data. Please try again.")
        else:
            st.warning("Please enter some text.")

st.divider()

clips = get_clips()

if not clips:
    st.info("No clips found yet.")
else:
    # Sort clips by id descending (newest first)
    sorted_clips = sorted(clips, key=lambda c: c['id'], reverse=True)
    selected = st.sidebar.selectbox("Select a clip", [f"{c['id']} - {c['summary'][:40]}" for c in sorted_clips])
    clip_id = int(selected.split(" - ")[0])
    details = get_clip_details(clip_id)

    st.subheader(f"Clip #{clip_id}")
    st.caption(f"📆 Date: {details.get('date')}")
    st.write(f"**Summary:** {details.get('summary', '')}")
    st.write("📝 Full Text")
    st.write(details.get("text", ""))