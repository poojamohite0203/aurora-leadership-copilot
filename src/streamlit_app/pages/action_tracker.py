import streamlit as st
from utils.api_client import get_action_items
from sidebar import render_sidebar

st.set_page_config(page_title="Action Tracker", layout="wide")
st.title("✅ Action Items Tracker")

render_sidebar()

actions = get_action_items()

if not actions:
    st.info("No action items.")
else:
    for a in actions:
        st.write(f"- {a['description']} (due: {a.get('due_date','N/A')})")