from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TradeBase(BaseModel):
    symbol: str
    side: str
    quantity: float
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    state: Optional[str] = "pending"
    open_timestamp: Optional[datetime] = None
    close_timestamp: Optional[datetime] = None
    trading_session: Optional[str] = None
    strategy_id: Optional[int] = None
    plan_id: Optional[int] = None
    risk_reward_ratio: Optional[float] = None
    pre_trade_emotion: Optional[str] = None
    post_trade_emotion: Optional[str] = None
    day_of_week: Optional[int] = None

class TradeCreate(TradeBase):
    account_id: int

class TradeRead(TradeBase):
    id: int
    account_id: int
    user_id: int
    pnl: Optional[float] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    state: Optional[str] = None
    open_timestamp: Optional[datetime] = None
    close_timestamp: Optional[datetime] = None
    trading_session: Optional[str] = None
    strategy_id: Optional[int] = None
    plan_id: Optional[int] = None
    risk_reward_ratio: Optional[float] = None
    pnl: Optional[float] = None
    outcome: Optional[str] = None
    pre_trade_emotion: Optional[str] = None
    post_trade_emotion: Optional[str] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
