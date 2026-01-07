from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trade(Base):
    """
    Rule 1: Every trade must belong to a known user and account.
    Rule 14: Strict ownership enforced via non-nullable user_id.
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    
    # FIX: Changed nullable=True to False to enforce Auth rules
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)

    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    state = Column(String(20), default="pending")  # pending, executed, closed etc.
    open_timestamp = Column(DateTime(timezone=True), nullable=True)
    close_timestamp = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Rule 13: Clean relationships
    account = relationship("Account", backref="trades")
    user = relationship("User", backref="trades")
