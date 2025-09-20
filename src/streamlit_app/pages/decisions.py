import streamlit as st
from utils.api_client import get_decisions, update_decision_status
from sidebar import render_sidebar

st.set_page_config(page_title="Decisions", layout="wide")
render_sidebar()
st.title("🗳 Decisions")

# Quick legend for first-time users
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- <b>🔴 Open</b>: Not decided yet<br>
- <b>✅ Decided</b>: Decision made<br>
- <b>🚀 Implemented</b>: Actioned<br>
- <b>❌ Cancelled</b>: No longer pursued<br><br>
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
    for decision in decisions:
        cols = st.columns([0.5, 4, 1.2, 2])
        status = decision.get('status', 'open')
        status_colors = {
            'open': '🔴',
            'decided': '✅',
            'implemented': '🚀',
            'cancelled': '❌'
        }
        status_icon = status_colors.get(status, '❓')
        with cols[0]:
            st.markdown(f"<span style='font-size:1.5em;'>{status_icon}</span>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{decision['description']}**", unsafe_allow_html=True)
            if decision.get('other_options'):
                st.caption(f"Options: {', '.join(decision['other_options'])}")
        with cols[2]:
            st.caption(f"Status: {status.replace('_', ' ').title()}")
        with cols[3]:
            new_status = st.selectbox(
                "",
                options=['open', 'decided', 'implemented', 'cancelled'],
                index=['open', 'decided', 'implemented', 'cancelled'].index(status),
                key=f"status_{decision['id']}"
            )
            if st.button("Update", key=f"update_{decision['id']}"):
                if new_status != status:
                    result = update_decision_status(decision['id'], new_status)
                    if result:
                        st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                        st.rerun()
                    else:
                        st.error("Failed to update status")
        st.markdown("---", unsafe_allow_html=True)
