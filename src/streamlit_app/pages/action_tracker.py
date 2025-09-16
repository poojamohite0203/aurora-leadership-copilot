import streamlit as st
from utils.api_client import get_action_items, update_action_item_status
from sidebar import render_sidebar

st.set_page_config(page_title="Action Tracker", layout="wide")
render_sidebar()
st.title("✅ Action Items Tracker")

# Status filter toggle
include_archived = st.toggle("Show Archived Items (done/ignored)", value=False)

# Get actions with status filter
actions = get_action_items(include_archived=include_archived)

if not actions:
    st.info("No action items found.")
else:
    for action in actions:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Status badge
                status = action.get('status', 'open')
                status_colors = {
                    'open': '🔴',
                    'in_progress': '🟡', 
                    'done': '✅',
                    'ignored': '⚫'
                }
                status_icon = status_colors.get(status, '❓')
                
                st.write(f"{status_icon} **{action['description']}**")
                if action.get('due_date'):
                    st.caption(f"Due: {action['due_date']}")
            
            with col2:
                st.write(f"Status: {status.replace('_', ' ').title()}")
            
            with col3:
                # Status update dropdown
                new_status = st.selectbox(
                    "Change Status",
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
            
            st.divider()