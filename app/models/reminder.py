from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    reminder_type = Column(String(50), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    time_utc = Column(Time, nullable=True)
    days_of_week = Column(String(20), nullable=True)
    message = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="reminders")

    def __repr__(self):
        return f"<Reminder(id={self.id}, type={self.reminder_type})>"
