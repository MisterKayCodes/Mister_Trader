import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Rule 4: Explicit Enums for Known States (Rule 1)
class DisciplineLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ConfidenceLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TradePsychology(Base):
    """
    Rule 1: System is in a known state.
    Rule 5: Unique trade_id ensures idempotency.
    """
    __tablename__ = "trade_psychology"

    id = Column(Integer, primary_key=True, index=True)
    
    trade_id = Column(
        Integer, 
        ForeignKey("trades.id", ondelete="CASCADE"), 
        nullable=False, 
        unique=True, 
        index=True
    )

    discipline = Column(Enum(DisciplineLevel), nullable=False)
    confidence = Column(Enum(ConfidenceLevel), nullable=False)
    followed_plan = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # Rule 13: Explicit relationship
    trade = relationship("Trade", backref="psychology", uselist=False)

    def __repr__(self):
        return f"<TradePsychology(trade_id={self.trade_id}, discipline={self.discipline.value})>"
