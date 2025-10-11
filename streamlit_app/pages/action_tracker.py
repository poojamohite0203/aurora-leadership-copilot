import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize database BEFORE any imports that might query it
from streamlit_app.utils.db_init import ensure_db_initialized
if "db_initialized" not in st.session_state:
    ensure_db_initialized()
    st.session_state["db_initialized"] = True

import streamlit as st
from streamlit_app.utils.api_client import get_action_items, update_action_item_status
from streamlit_app.sidebar import render_sidebar
import pandas as pd

st.set_page_config(page_title="Action Tracker", layout="wide")
render_sidebar()
st.title("✅ Action Items Tracker")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- <b>🟠 Open</b>: Not started yet<br>
- <b>🟦 In Progress</b>: Work is ongoing<br>
- <b>✅ Done</b>: Completed<br>
- <b>⚪ Ignored</b>: No longer relevant<br><br>
Use the <b>Change Status</b> dropdown to update an action item's status.<br>
Toggle <b>Show Archived Items</b> to view completed or ignored items.
</div>
""", unsafe_allow_html=True)

# Status filter toggle
include_archived = st.toggle("Show Archived Items (done/ignored)", value=False)

# Get actions with status filter
actions = get_action_items(include_archived=include_archived)

if not actions:
    st.info("No action items found.")
else:
    status_colors = {
        'open': '🟠',
        'in_progress': '🟦',
        'done': '✅',
        'ignored': '⚪'
    }
    # Table header
    cols = st.columns([0.7, 4, 1.5, 2, 1])
    headers = ["Status", "Description", "Current Status", "Change Status", "Update"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    # Table rows
    for action_item in actions:
        status = action_item.get('status', 'open') if isinstance(action_item, dict) else getattr(action_item, 'status', 'open')
        description = action_item.get('description', '') if isinstance(action_item, dict) else getattr(action_item, 'description', '')
        action_item_id = action_item.get('id', None) if isinstance(action_item, dict) else getattr(action_item, 'id', None)
        with st.container():
            cols = st.columns([0.7, 4, 1.5, 2, 1])
            with cols[0]:
                st.markdown(status_colors.get(status, '❓'))
            with cols[1]:
                st.markdown(description)
                if hasattr(action_item, 'due_date') and action_item.due_date:
                    st.caption(f"Due: {action_item.due_date}")
            with cols[2]:
                st.caption(status.replace('_', ' ').title())
            with cols[3]:
                new_status = st.selectbox(
                    "Change Status",  # Non-empty label for accessibility
                    options=['open', 'in_progress', 'done', 'ignored'],
                    index=['open', 'in_progress', 'done', 'ignored'].index(status),
                    key=f"status_{action_item_id}"
                )
            with cols[4]:
                if st.button("Update", key=f"update_{action_item_id}"):
                    if new_status != status:
                        result = update_action_item_status(action_item_id, new_status)
                        if result:
                            st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                            st.rerun()
                        else:
                            st.error("Failed to update status")