"""
Shared initialization module for Streamlit pages.
Ensures database is initialized before any page queries.
"""
import sys
import os
import streamlit as st

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )

# Initialize database tables (safe to call multiple times)
from src.db.init_db import init_database

# Only initialize once per Streamlit session
_db_initialized = st.session_state.get("db_initialized", False)

def ensure_db_initialized():
    """Ensure database is initialized before any database operations."""
    global _db_initialized
    if not _db_initialized:
        try:
            result = init_database()
            st.session_state["db_initialized"] = True
            _db_initialized = True
            return result
        except Exception as e:
            print(f"Database initialization failed: {e}")
            return False
    return True

# Auto-initialize when imported
ensure_db_initialized()
