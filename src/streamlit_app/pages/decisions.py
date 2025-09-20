import streamlit as st
from utils.api_client import get_decisions, update_decision_status
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
    table_data = []
    status_colors = {
        'open': '🟠',
        'decided': '✅',
        'implemented': '🚀',
        'cancelled': '⚪'
    }
    for decision in decisions:
        table_data.append({
            'Status': status_colors.get(decision.get('status', 'open'), '❓'),
            'Description': decision['description'],
            'Current Status': decision.get('status', '').replace('_', ' ').title(),
            'ID': decision['id']
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df.drop(columns=['ID']), use_container_width=True)
    for decision in decisions:
        new_status = st.selectbox(
            f"Change Status for: {decision['description'][:30]}",
            options=['open', 'decided', 'implemented', 'cancelled'],
            index=['open', 'decided', 'implemented', 'cancelled'].index(decision.get('status', 'open')),
            key=f"status_{decision['id']}"
        )
        if st.button("Update", key=f"update_{decision['id']}"):
            if new_status != decision.get('status', 'open'):
                result = update_decision_status(decision['id'], new_status)
                if result:
                    st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                    st.rerun()
                else:
                    st.error("Failed to update status")
