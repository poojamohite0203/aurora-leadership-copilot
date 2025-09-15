import streamlit as st
from utils.api_client import ask_ai

st.set_page_config(page_title="Ask Assistant", layout="wide")
st.title("🤖 Ask Assistant")

query = st.text_area("Ask a question about your meetings, journals, or clips")

if st.button("Ask"):
    if query.strip():
        answer = ask_ai(query)
        st.subheader("Answer")
        st.write(answer["answer"])
        with st.expander("Context Used"):
            for c in answer.get("contexts", []):
                st.write(f"- [{c['metadata']['type']}] {c['text']}")
    else:
        st.warning("Please enter a question.")
