import streamlit as st
from utils.api_client import get_blockers
from sidebar import render_sidebar

st.set_page_config(page_title="Blockers", layout="wide")
st.title("⛔ Blockers")

render_sidebar()

blockers = get_blockers()

if not blockers:
    st.info("No blockers.")
else:
    for b in blockers:
        st.write(f"- {b['description']}")