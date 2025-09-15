import streamlit as st
from utils.api_client import get_decisions
from sidebar import render_sidebar

st.set_page_config(page_title="Decisions", layout="wide")
st.title("🗳 Decisions")

render_sidebar()

decisions = get_decisions()

if not decisions:
    st.info("No decisions.")
else:
    for d in decisions:
        st.write(f"- {d['description']} | Options: {', '.join(d.get('other_options', []))}")
