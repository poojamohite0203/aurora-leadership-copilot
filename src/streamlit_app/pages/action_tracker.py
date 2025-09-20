import streamlit as st
from utils.api_client import get_action_items, update_action_item_status
from sidebar import render_sidebar
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
    # Prepare table data
    table_data = []
    status_colors = {
        'open': '🟠',
        'in_progress': '🟦',
        'done': '✅',
        'ignored': '⚪'
    }
    for action in actions:
        table_data.append({
            'Status': status_colors.get(action.get('status', 'open'), '❓'),
            'Description': action['description'],
            'Due Date': action.get('due_date', ''),
            'Current Status': action.get('status', '').replace('_', ' ').title(),
            'ID': action['id']
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df.drop(columns=['ID']), use_container_width=True)
    # Status update controls
    for action in actions:
        new_status = st.selectbox(
            f"Change Status for: {action['description'][:30]}",
            options=['open', 'in_progress', 'done', 'ignored'],
            index=['open', 'in_progress', 'done', 'ignored'].index(action.get('status', 'open')),
            key=f"status_{action['id']}"
        )
        if st.button("Update", key=f"update_{action['id']}"):
            if new_status != action.get('status', 'open'):
                result = update_action_item_status(action['id'], new_status)
                if result:
                    st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                    st.rerun()
                else:
                    st.error("Failed to update status")