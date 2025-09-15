# ui/pages/action_items.py
import streamlit as st
from utils.api_client import get_action_items

st.set_page_config(page_title="Action Tracker", layout="wide")
st.title("✅ Action Items Tracker")

actions = get_action_items()

if not actions:
    st.info("No action items.")
else:
    for a in actions:
        st.write(f"- {a['description']} (due: {a.get('due_date','N/A')})")