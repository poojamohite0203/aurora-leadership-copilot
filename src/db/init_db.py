"""
Database initialization module.
Import all models and create tables.
"""

def init_database():
    """Initialize the database by importing all models and creating tables."""
    # Import all models so SQLAlchemy knows about them
    from . import models  # This imports all model classes
    from .database import create_tables
    
    # Create all tables
    create_tables()
    
    return True

# Auto-initialize when this module is imported
if __name__ != "__main__":
    init_database()
