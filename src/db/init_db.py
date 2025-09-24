"""
Database initialization module.
Import all models and create tables.
"""

def init_database():
    """Initialize the database by importing all models and creating tables."""
    try:
        print("🔧 Starting database initialization...")
        
        # Import all models so SQLAlchemy knows about them
        from . import models  # This imports all model classes
        print("✅ Models imported successfully")
        
        from .database import create_tables, engine
        print("✅ Database engine loaded")
        
        # Create all tables
        create_tables()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Database initialized with tables: {tables}")
        
        if not tables:
            print("❌ WARNING: No tables were created!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Auto-initialize when this module is imported
if __name__ != "__main__":
    result = init_database()
    if not result:
        print("❌ Database initialization failed during import!")
