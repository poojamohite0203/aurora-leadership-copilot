from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME = "app_data.db"  # Your SQLite DB filename
DB_PATH = os.path.join(BASE_DIR, DB_FILENAME)

# Auto-create DB if missing
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'a').close()  # just touch the file

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# For SQLite, check_same_thread=False is required for multiple threads (like Streamlit)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
