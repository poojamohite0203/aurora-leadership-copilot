import streamlit as st
from utils.api_client import get_action_items, update_action_item_status
from sidebar import render_sidebar

st.set_page_config(page_title="Action Tracker", layout="wide")
render_sidebar()
st.title("✅ Action Items Tracker")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- <b>🔴 Open</b>: Not started yet<br>
- <b>🟡 In Progress</b>: Work is ongoing<br>
- <b>✅ Done</b>: Completed<br>
- <b>⚫ Ignored</b>: No longer relevant<br><br>
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
    for action in actions:
        cols = st.columns([0.5, 4, 1.2, 2])
        status = action.get('status', 'open')
        status_colors = {
            'open': '🔴',
            'in_progress': '🟡', 
            'done': '✅',
            'ignored': '⚫'
        }
        status_icon = status_colors.get(status, '❓')
        with cols[0]:
            st.markdown(f"<span style='font-size:1.5em;'>{status_icon}</span>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{action['description']}**", unsafe_allow_html=True)
            if action.get('due_date'):
                st.caption(f"Due: {action['due_date']}")
        with cols[2]:
            st.caption(f"Status: {status.replace('_', ' ').title()}")
        with cols[3]:
            new_status = st.selectbox(
                "",
                options=['open', 'in_progress', 'done', 'ignored'],
                index=['open', 'in_progress', 'done', 'ignored'].index(status),
                key=f"status_{action['id']}"
            )
            if st.button("Update", key=f"update_{action['id']}"):
                if new_status != status:
                    result = update_action_item_status(action['id'], new_status)
                    if result:
                        st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                        st.rerun()
                    else:
                        st.error("Failed to update status")
        st.markdown("---", unsafe_allow_html=True)