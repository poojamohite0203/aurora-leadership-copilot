import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize database BEFORE any other imports
from streamlit_app.utils.db_init import ensure_db_initialized
ensure_db_initialized()

import streamlit as st
from streamlit_app.utils.backend_client import get_weekly_reports, generate_weekly_report
from sidebar import render_sidebar
import datetime

st.set_page_config(page_title="Weekly Reports", layout="wide")
st.title("📊 Weekly Status Reports")

# Quick legend and dashboard summary
st.markdown("""
<div style='background-color:#f0f2f6; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>How to use:</b><br>
- Each report summarizes your meetings, action items, blockers, and decisions for the week.<br>
- Click a week to expand and view the summary.<br>
- Download the report for sharing or record-keeping.<br>
</div>
""", unsafe_allow_html=True)

render_sidebar()

reports = get_weekly_reports()

# --- Weekly Report Generation UI ---
st.markdown("""
<div style='background-color:#e6f7ff; color:#222; padding:10px; border-radius:8px; margin-bottom:16px;'>
<b>Generate a new weekly report:</b><br>
Select any date within the week you want to generate a report for. The system will summarize all meetings, action items, blockers, and decisions for that week.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])
def_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
with col1:
    selected_date = st.date_input("Select a date in the week", value=def_date, max_value=datetime.date.today())
with col2:
    if 'gen_loading' not in st.session_state:
        st.session_state['gen_loading'] = False
    gen_btn = st.button("Generate Report", disabled=st.session_state['gen_loading'])

if gen_btn:
    st.session_state['gen_loading'] = True
    with st.spinner("Generating weekly report..."):
        # Ensure date is formatted as YYYY-MM-DD string
        date_str = selected_date.strftime("%Y-%m-%d")
        result = generate_weekly_report(date_str, True)
    st.session_state['gen_loading'] = False
    if result.get("error"):
        st.error(f"Failed to generate report: {result['error']}")
    elif result.get("summary"):
        st.success("Report generated!")
        st.rerun()
    else:
        st.warning("No new report generated (possibly already exists for this week).")

if not reports:
    st.info("No reports generated yet.")
else:
    # Dashboard stats
    st.markdown(f"**Total Reports:** {len(reports)}")
    st.markdown(f"**Most Recent Week:** {reports[-1]['week_start']} → {reports[-1]['week_end']}")
    st.divider()
    for r in reversed(reports):
        with st.expander(f"Week of {r['week_start']} → {r['week_end']}"):
            # Clean up summary display - handle both old JSON format and new plain text
            summary = r["summary"]
            if summary.strip().startswith('{"summary":'):
                try:
                    import json
                    parsed = json.loads(summary)
                    summary = parsed.get("summary", summary)
                except:
                    pass
            elif '"summary":' in summary:
                import re
                match = re.search(r'"summary":\s*"([^"]+)"', summary)
                if match:
                    summary = match.group(1)
            
            st.write(summary)
            st.download_button(
                "Download Report",
                summary,
                file_name=f"weekly_report_{r['week_start']}.txt",
                key=f"download_{r['week_start']}"
            )