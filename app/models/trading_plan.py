from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class TradingPlan(Base):
    __tablename__ = "trading_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(200), nullable=False)
    plan_date = Column(Date, nullable=True)
    market_bias = Column(String(50), nullable=True)
    key_levels = Column(Text, nullable=True)
    watchlist = Column(Text, nullable=True)
    news_events = Column(Text, nullable=True)
    mental_state = Column(String(100), nullable=True)
    max_trades = Column(Integer, nullable=True)
    max_loss = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="trading_plans")

    def __repr__(self):
        return f"<TradingPlan(id={self.id}, title={self.title})>"
