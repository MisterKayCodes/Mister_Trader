from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class DisciplineLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConfidenceLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TradePsychology(Base):
    __tablename__ = "trade_psychology"

    id = Column(Integer, primary_key=True, index=True)

    trade_id = Column(
        Integer,
        ForeignKey("trades.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    discipline = Column(Enum(DisciplineLevel), nullable=False)

    confidence = Column(Enum(ConfidenceLevel), nullable=False)

    followed_plan = Column(Boolean, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship
    trade = relationship("Trade", backref="psychology", uselist=False)
