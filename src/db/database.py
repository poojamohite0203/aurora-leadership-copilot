from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render.com detection and database path
IS_RENDER = os.environ.get("RENDER") is not None
IS_LOCAL = not IS_RENDER

if IS_RENDER:
    # Render.com - use persistent disk storage
    DB_PATH = "/app/data/aurora.db"
    print("🚀 Running on Render.com - using persistent database")
else:
    # Local development
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "aurora.db")
    print("💻 Local development mode")

# Ensure directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Auto-create DB if missing
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'a').close()
    print(f"📄 Created new database at: {DB_PATH}")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLite configuration optimized for web deployment
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={
        "check_same_thread": False,
        "timeout": 20  # Add timeout for better reliability
    },
    pool_pre_ping=True,  # Verify connections before use
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    """Create all database tables. Call this after importing all models."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()