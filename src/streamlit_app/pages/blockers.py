import streamlit as st
from utils.api_client import get_blockers, update_blocker_status
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
    table_data = []
    status_colors = {
        'open': '🟠',
        'in_progress': '🟦',
        'resolved': '✅',
        'escalated': '🚨',
        'ignored': '⚪'
    }
    for blocker in blockers:
        table_data.append({
            'Status': status_colors.get(blocker.get('status', 'open'), '❓'),
            'Description': blocker['description'],
            'Current Status': blocker.get('status', '').replace('_', ' ').title(),
            'ID': blocker['id']
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df.drop(columns=['ID']), use_container_width=True)
    for blocker in blockers:
        new_status = st.selectbox(
            f"Change Status for: {blocker['description'][:30]}",
            options=['open', 'in_progress', 'resolved', 'escalated', 'ignored'],
            index=['open', 'in_progress', 'resolved', 'escalated', 'ignored'].index(blocker.get('status', 'open')),
            key=f"status_{blocker['id']}"
        )
        if st.button("Update", key=f"update_{blocker['id']}"):
            if new_status != blocker.get('status', 'open'):
                result = update_blocker_status(blocker['id'], new_status)
                if result:
                    st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                    st.rerun()
                else:
                    st.error("Failed to update status")