import streamlit as st
from utils.api_client import get_blockers, update_blocker_status
from sidebar import render_sidebar

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
    for blocker in blockers:
        cols = st.columns([0.5, 4, 1.2, 2])
        status = blocker.get('status', 'open')
        status_colors = {
            'open': '🟠',
            'in_progress': '🟦',
            'resolved': '✅',
            'escalated': '🚨',
            'ignored': '⚪'
        }
        status_icon = status_colors.get(status, '❓')
        with cols[0]:
            st.markdown(f"<span style='font-size:1.5em;'>{status_icon}</span>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{blocker['description']}**", unsafe_allow_html=True)
        with cols[2]:
            st.caption(f"Status: {status.replace('_', ' ').title()}")
        with cols[3]:
            new_status = st.selectbox(
                "",
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
        st.markdown("---", unsafe_allow_html=True)