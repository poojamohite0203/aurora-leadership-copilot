import sys
import os
import streamlit as st


# Add project root to Python path FIRST
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize database BEFORE any other imports
from streamlit_app.utils.db_init import ensure_db_initialized
if "db_initialized" not in st.session_state:
    ensure_db_initialized()
    st.session_state["db_initialized"] = True

import streamlit as st
from streamlit_app.utils.api_client import search_items
from streamlit_app.sidebar import render_sidebar

# Render the custom sidebar
render_sidebar()

st.set_page_config(page_title="Search", layout="wide")
st.title("🔍 Search Knowledge Base")

query = st.text_input("Enter your search query")

if query:
    response = search_items(query)
    if not response or not response.get("results"):
        st.warning("No matches found.")
    else:
        results = response.get("results", [])
        st.info(f"Found {response.get('total_results', len(results))} results for: '{query}'")
        
        for r in results:
            # Safely access metadata with fallbacks
            metadata = r.get('metadata', {})
            item_type = metadata.get('type', 'unknown') if metadata else 'unknown'
            text = r.get('text', 'No content available')
            similarity = r.get('similarity_score')
            
            # Display the result
            st.write(f"**[{item_type}]** {text}")
            if similarity is not None:
                st.caption(f"Similarity score: {similarity:.3f}")
            st.divider()
