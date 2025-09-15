import streamlit as st
from utils.api_client import get_blockers

st.set_page_config(page_title="Blockers", layout="wide")
st.title("⛔ Blockers")

blockers = get_blockers()

if not blockers:
    st.info("No blockers.")
else:
    for b in blockers:
        st.write(f"- {b['description']}")