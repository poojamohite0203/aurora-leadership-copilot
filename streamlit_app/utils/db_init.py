"""
Shared initialization module for Streamlit pages.
Ensures database is initialized before any page queries.
"""
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize database tables (safe to call multiple times)
from src.db.init_db import init_database

def ensure_db_initialized():
    """Ensure database is initialized before any database operations."""
    try:
        return init_database()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False

# Auto-initialize when imported
ensure_db_initialized()
