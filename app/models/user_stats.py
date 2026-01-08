from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    total_trades = Column(Integer, default=0, nullable=False)
    winning_trades = Column(Integer, default=0, nullable=False)
    losing_trades = Column(Integer, default=0, nullable=False)
    breakeven_trades = Column(Integer, default=0, nullable=False)
    
    total_pnl = Column(Float, default=0.0, nullable=False)
    best_trade_pnl = Column(Float, default=0.0, nullable=False)
    worst_trade_pnl = Column(Float, default=0.0, nullable=False)
    
    current_streak = Column(Integer, default=0, nullable=False)
    current_streak_type = Column(String(10), nullable=True)
    best_win_streak = Column(Integer, default=0, nullable=False)
    worst_loss_streak = Column(Integer, default=0, nullable=False)
    
    avg_risk_reward = Column(Float, default=0.0, nullable=False)
    
    london_wins = Column(Integer, default=0, nullable=False)
    london_losses = Column(Integer, default=0, nullable=False)
    newyork_wins = Column(Integer, default=0, nullable=False)
    newyork_losses = Column(Integer, default=0, nullable=False)
    asian_wins = Column(Integer, default=0, nullable=False)
    asian_losses = Column(Integer, default=0, nullable=False)
    sydney_wins = Column(Integer, default=0, nullable=False)
    sydney_losses = Column(Integer, default=0, nullable=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="stats")

    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, total_trades={self.total_trades})>"
