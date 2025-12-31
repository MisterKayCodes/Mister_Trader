from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class TradeState(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class VoiceNote(Base):
    __tablename__ = "trade_voice_notes"

    id = Column(Integer, primary_key=True, index=True)

    trade_id = Column(
        Integer,
        ForeignKey("trades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_path = Column(String, nullable=False)

    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    trade_state_at_time = Column(Enum(TradeState), nullable=False)

    # Relationship
    trade = relationship("Trade", backref="voice_notes")
