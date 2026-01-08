from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Rule 1: Force SQLite for Replit environment to ensure stability and user-controlled data.
# We bypass settings.DATABASE_URL if it's pointing to a system-managed Postgres secret.
DATABASE_URL = "sqlite:///./mister_trader.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    """Rule 7: Standard session lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
