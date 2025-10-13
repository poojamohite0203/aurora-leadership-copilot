"""
Database initialization module.
Import all models and create tables.
"""

_db_initialized = False

def init_database():
    """Initialize the database by importing all models and creating tables."""
    global _db_initialized
    if _db_initialized:
        return True
    try:
        print("🔧 Starting database initialization...")
        
        # Import all models so SQLAlchemy knows about them
        from . import models  # This imports all model classes
        from .database import create_tables, engine
        
        # Create all tables
        create_tables()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("❌ WARNING: No tables were created!")
            return False
            
        _db_initialized = True
        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False
