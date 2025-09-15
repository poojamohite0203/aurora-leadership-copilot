import streamlit as st
from utils.api_client import search_items

st.set_page_config(page_title="Search", layout="wide")
st.title("🔍 Search Knowledge Base")

query = st.text_input("Enter your search query")

if query:
    results = search_items(query)
    if not results:
        st.warning("No matches found.")
    else:
        for r in results:
            st.write(f"**[{r['metadata']['type']}]** {r['text']}")
