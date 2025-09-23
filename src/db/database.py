from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use /tmp for Streamlit Cloud, fallback to local for local dev
if os.environ.get("STREAMLIT_CLOUD", "0") == "1":
    DATABASE_URL = "sqlite:////tmp/aurora.db"
else:
    DATABASE_URL = "sqlite:///./aurora.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
