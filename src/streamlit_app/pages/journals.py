# ui/pages/journals.py
import streamlit as st
from utils.api_client import get_journals, get_journal_details

st.set_page_config(page_title="Journals", layout="wide")
st.title("📔 Journals")

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
