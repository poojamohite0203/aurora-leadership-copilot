import streamlit as st
from utils.api_client import search_items

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
