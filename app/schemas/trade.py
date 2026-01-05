from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TradeBase(BaseModel):
    symbol: str
    side: str
    quantity: float
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    state: Optional[str] = "pending"
    open_timestamp: Optional[datetime] = None
    close_timestamp: Optional[datetime] = None

class TradeCreate(TradeBase):
    account_id: int
    user_id: Optional[int] = None  # if you want to allow setting this on create

class TradeRead(TradeBase):
    id: int
    account_id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    state: Optional[str] = None
    open_timestamp: Optional[datetime] = None
    close_timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
