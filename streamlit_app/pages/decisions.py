import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from streamlit_app.utils.backend_client import get_decisions, update_decision_status
from sidebar import render_sidebar
import pandas as pd

st.set_page_config(page_title="Decisions", layout="wide")
render_sidebar()
st.title("🗳 Decisions")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- <b>🟠 Open</b>: Not decided yet<br>
- <b>✅ Decided</b>: Decision made<br>
- <b>🚀 Implemented</b>: Actioned<br>
- <b>⚪ Cancelled</b>: No longer pursued<br><br>
Use the <b>Change Status</b> dropdown to update a decision's status.<br>
Toggle <b>Show Archived Decisions</b> to view decided or cancelled items.
</div>
""", unsafe_allow_html=True)

# Status filter toggle
include_archived = st.toggle("Show Archived Decisions (decided/cancelled)", value=False)

# Get decisions with status filter
decisions = get_decisions(include_archived=include_archived)

if not decisions:
    st.info("No decisions found.")
else:
    status_colors = {
        'open': '🟠',
        'decided': '✅',
        'implemented': '🚀',
        'cancelled': '⚪'
    }
    # Table header
    cols = st.columns([0.7, 4, 1.5, 2, 1])
    headers = ["Status", "Description", "Current Status", "Change Status", "Update"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    # Table rows
    for decision in decisions:
        status = decision.status if hasattr(decision, 'status') else getattr(decision, 'status', 'open')
        with st.container():
            cols = st.columns([0.7, 4, 1.5, 2, 1])
            with cols[0]:
                st.markdown(status_colors.get(status, '❓'))
            with cols[1]:
                st.markdown(decision.description)
            with cols[2]:
                st.caption(status.replace('_', ' ').title())
            with cols[3]:
                new_status = st.selectbox(
                    "Change Status",  # Non-empty label for accessibility
                    options=['open', 'decided', 'implemented', 'cancelled'],
                    index=['open', 'decided', 'implemented', 'cancelled'].index(status),
                    key=f"status_{decision.id}"
                )
            with cols[4]:
                if st.button("Update", key=f"update_{decision.id}"):
                    if new_status != status:
                        result = update_decision_status(decision.id, new_status)
                        if result:
                            st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                            st.rerun()
                        else:
                            st.error("Failed to update status")
