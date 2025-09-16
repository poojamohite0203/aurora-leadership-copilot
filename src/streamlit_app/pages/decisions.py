import streamlit as st
from utils.api_client import get_decisions, update_decision_status
from sidebar import render_sidebar

st.set_page_config(page_title="Decisions", layout="wide")
render_sidebar()
st.title("🗳 Decisions")

# Status filter toggle
include_archived = st.toggle("Show Archived Decisions (decided/cancelled)", value=False)

# Get decisions with status filter
decisions = get_decisions(include_archived=include_archived)

if not decisions:
    st.info("No decisions found.")
else:
    for decision in decisions:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Status badge
                status = decision.get('status', 'open')
                status_colors = {
                    'open': '🔴',
                    'decided': '✅',
                    'implemented': '🚀',
                    'cancelled': '❌'
                }
                status_icon = status_colors.get(status, '❓')
                
                st.write(f"{status_icon} **{decision['description']}**")
                if decision.get('other_options'):
                    st.caption(f"Options: {', '.join(decision['other_options'])}")
            
            with col2:
                st.write(f"Status: {status.replace('_', ' ').title()}")
            
            with col3:
                # Status update dropdown
                new_status = st.selectbox(
                    "Change Status",
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
            
            st.divider()
