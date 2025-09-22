import streamlit as st
from utils.api_client import get_journals, get_journal_details, extract_journal
from sidebar import render_sidebar

st.set_page_config(page_title="Journals", layout="wide")
st.title("📔 Journals")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- Add new journal entries using the form above.<br>
- View and select past journals from the sidebar.<br>
- Explore extracted <b>Growth Areas</b>, <b>Strengths</b>, and <b>Themes</b> in each entry.<br>
</div>
""", unsafe_allow_html=True)

# Render the custom sidebar
render_sidebar()

# Add new journal section
st.header("➕ Agetdd New Journal Entry")
with st.expander("Add Journal Entry", expanded=False):
    if "journal_text" not in st.session_state:
        st.rerun()
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
