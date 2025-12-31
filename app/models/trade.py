from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Float,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class TradeState(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    symbol = Column(String(20), nullable=False)

    direction = Column(Enum("BUY", "SELL", name="direction_enum"), nullable=False)

    entry_price = Column(Float, nullable=False)

    exit_price = Column(Float, nullable=True)

    state = Column(Enum(TradeState), nullable=False, index=True)

    open_timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    close_timestamp = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships (string refs, no direct import)
    user = relationship("User", backref="trades")
    account = relationship("Account", backref="trades")
