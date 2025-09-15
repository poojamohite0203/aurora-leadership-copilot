import streamlit as st
from utils.api_client import get_clips, get_clip_details, extract_clip

st.set_page_config(page_title="Clips", layout="wide")
st.title("📋 Clipboard History")

# Add new clip section
st.header("➕ Add New Clip")
with st.expander("Add Text Clip", expanded=False):
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
                    st.rerun()  # Refresh the page to show the new clip
                else:
                    st.error("❌ Failed to extract clip data. Please try again.")
        else:
            st.warning("Please enter some text.")

st.divider()

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