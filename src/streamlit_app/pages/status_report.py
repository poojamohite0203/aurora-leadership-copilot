import streamlit as st
from utils.api_client import get_weekly_reports
from sidebar import render_sidebar

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

if not reports:
    st.info("No reports generated yet.")
else:
    # Dashboard stats
    st.markdown(f"**Total Reports:** {len(reports)}")
    st.markdown(f"**Most Recent Week:** {reports[-1]['week_start']} → {reports[-1]['week_end']}")
    st.divider()
    for r in reversed(reports):
        with st.expander(f"Week of {r['week_start']} → {r['week_end']}"):
            st.write(r["summary"])
            st.download_button("Download Report", r["summary"], file_name=f"weekly_report_{r['week_start']}.txt")