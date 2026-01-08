from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings 

# Rule 1: Using a verified, known state from settings
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    # Rule 13: Standard 2026 SQLite handling
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    """Rule 7: Ensure session recovery and closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
