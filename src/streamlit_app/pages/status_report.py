import streamlit as st
from utils.api_client import get_weekly_reports

st.set_page_config(page_title="Weekly Reports", layout="wide")
st.title("📊 Weekly Status Reports")

reports = get_weekly_reports()

if not reports:
    st.info("No reports generated yet.")
else:
    for r in reports:
        with st.expander(f"Week of {r['week_start']} → {r['week_end']}"):
            st.write(r["summary"])
            st.download_button("Download Report", r["summary"], file_name=f"weekly_report_{r['week_start']}.txt")