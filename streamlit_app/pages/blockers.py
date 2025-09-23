import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import streamlit as st
from streamlit_app.utils.backend_client import get_blockers, update_blocker_status
from sidebar import render_sidebar
import pandas as pd

st.set_page_config(page_title="Blockers", layout="wide")
render_sidebar()
st.title("⛔ Blockers")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- <b>🟠 Open</b>: Not yet resolved<br>
- <b>🟦 In Progress</b>: Being worked on<br>
- <b>✅ Resolved</b>: Fixed<br>
- <b>🚨 Escalated</b>: Needs urgent attention<br>
- <b>⚪ Ignored</b>: No longer relevant<br><br>
Use the <b>Change Status</b> dropdown to update a blocker's status.<br>
Toggle <b>Show Archived Blockers</b> to view resolved or ignored items.
</div>
""", unsafe_allow_html=True)

# Status filter toggle
include_archived = st.toggle("Show Archived Blockers (resolved/ignored)", value=False)

# Get blockers with status filter
blockers = get_blockers(include_archived=include_archived)

if not blockers:
    st.info("No blockers found.")
else:
    status_colors = {
        'open': '🟠',
        'in_progress': '🟦',
        'resolved': '✅',
        'escalated': '🚨',
        'ignored': '⚪'
    }
    # Table header
    cols = st.columns([0.7, 4, 1.5, 2, 1])
    headers = ["Status", "Description", "Current Status", "Change Status", "Update"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    # Table rows
    for blocker in blockers:
        status = blocker.status if hasattr(blocker, 'status') else getattr(blocker, 'status', 'open')
        with st.container():
            cols = st.columns([0.7, 4, 1.5, 2, 1])
            with cols[0]:
                st.markdown(status_colors.get(status, '❓'))
            with cols[1]:
                st.markdown(blocker.description)
            with cols[2]:
                st.caption(status.replace('_', ' ').title())
            with cols[3]:
                new_status = st.selectbox(
                    "Change Status",  # Non-empty label for accessibility
                    options=['open', 'in_progress', 'resolved', 'escalated', 'ignored'],
                    index=['open', 'in_progress', 'resolved', 'escalated', 'ignored'].index(status),
                    key=f"status_{blocker.id}"
                )
            with cols[4]:
                if st.button("Update", key=f"update_{blocker.id}"):
                    if new_status != status:
                        result = update_blocker_status(blocker.id, new_status)
                        if result:
                            st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                            st.rerun()
                        else:
                            st.error("Failed to update status")