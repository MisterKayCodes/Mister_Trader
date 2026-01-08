from sqlalchemy import Column, Integer, Date, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Activity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)

    date = Column(Date, nullable=False, index=True)

    activity_type = Column(String(50), nullable=False)  # e.g. "TRADE" or "ANALYSIS_ONLY"

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
