import streamlit as st
from utils.api_client import get_blockers, update_blocker_status
from sidebar import render_sidebar

st.set_page_config(page_title="Blockers", layout="wide")
render_sidebar()
st.title("⛔ Blockers")

# Status filter toggle
include_archived = st.toggle("Show Archived Blockers (resolved/ignored)", value=False)

# Get blockers with status filter
blockers = get_blockers(include_archived=include_archived)

if not blockers:
    st.info("No blockers found.")
else:
    for blocker in blockers:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Status badge
                status = blocker.get('status', 'open')
                status_colors = {
                    'open': '🔴',
                    'in_progress': '🟡',
                    'resolved': '✅',
                    'escalated': '🚨',
                    'ignored': '⚫'
                }
                status_icon = status_colors.get(status, '❓')
                
                st.write(f"{status_icon} **{blocker['description']}**")
            
            with col2:
                st.write(f"Status: {status.replace('_', ' ').title()}")
            
            with col3:
                # Status update dropdown
                new_status = st.selectbox(
                    "Change Status",
                    options=['open', 'in_progress', 'resolved', 'escalated', 'ignored'],
                    index=['open', 'in_progress', 'resolved', 'escalated', 'ignored'].index(status),
                    key=f"status_{blocker['id']}"
                )
                
                if st.button("Update", key=f"update_{blocker['id']}"):
                    if new_status != status:
                        result = update_blocker_status(blocker['id'], new_status)
                        if result:
                            st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                            st.rerun()
                        else:
                            st.error("Failed to update status")
            
            st.divider()