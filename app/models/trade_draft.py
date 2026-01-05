from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TradeDraft(Base):
    __tablename__ = "trade_drafts"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(
        Integer,
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)

    status = Column(String(20), default="draft")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    account = relationship("Account", backref="trade_drafts")
