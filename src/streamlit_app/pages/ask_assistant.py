import streamlit as st
from utils.api_client import ask_ai
from sidebar import render_sidebar

st.set_page_config(page_title="Ask Assistant", layout="wide")
render_sidebar()
st.title("🤖 Ask Assistant")

query = st.text_area("Ask a question about your meetings, journals, or clips")

if st.button("Ask"):
    if query.strip():
        response = ask_ai(query)
        st.subheader("Answer")
        st.write(response["answer"])
        
        # Display context used
        context_used = response.get("context_used", [])
        if context_used:
            with st.expander("Context Used"):
                for i, context in enumerate(context_used, 1):
                    st.write(f"{i}. {context}")
        else:
            st.info("No context was used for this answer.")
    else:
        st.warning("Please enter a question.")
