import streamlit as st
from utils.api_client import get_journals, get_journal_details, extract_journal

st.set_page_config(page_title="Journals", layout="wide")
st.title("📔 Journals")

# Add new journal section
st.header("➕ Add New Journal Entry")
with st.expander("Add Journal Entry", expanded=False):
    journal_text = st.text_area(
        "Enter journal entry:",
        placeholder="Write about your day, thoughts, learnings, challenges, wins, etc...",
        height=200,
        key="journal_text"
    )
    
    if st.button("Extract Journal Data", key="extract_journal"):
        if journal_text.strip():
            with st.spinner("Processing journal entry..."):
                result = extract_journal(journal_text)
                if result:
                    st.success(f"✅ Journal extracted successfully! Journal ID: {result.get('id', 'N/A')}")
                    st.rerun()  # Refresh the page to show the new journal
                else:
                    st.error("❌ Failed to extract journal data. Please try again.")
        else:
            st.warning("Please enter a journal entry.")

st.divider()

journals = get_journals()

if not journals:
    st.info("No journals found yet.")
else:
    selected = st.sidebar.selectbox("Select a journal", [f"{j['id']} - {j['summary'][:40]}" for j in journals])
    journal_id = int(selected.split(" - ")[0])
    details = get_journal_details(journal_id)

    st.subheader(f"Journal #{journal_id}")
    st.caption(f"📆 Date: {details.get('date')}")
    st.write(f"**Summary:** {details.get('summary', '')}")
    st.write("📝 Full Text")
    st.write(details.get("text", ""))

    with st.expander("🌱 Growth Areas"):
        st.write(details.get("growth_area", "N/A"))

    with st.expander("💪 Strengths"):
        st.write(details.get("strength", "N/A"))

    with st.expander("🎭 Themes"):
        st.write(details.get("theme", "N/A"))
