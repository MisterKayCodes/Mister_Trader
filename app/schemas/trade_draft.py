from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TradeDraftBase(BaseModel):
    symbol: str
    side: str
    quantity: float
    price: Optional[float] = None


class TradeDraftCreate(TradeDraftBase):
    account_id: int


class TradeDraftRead(TradeDraftBase):
    id: int
    account_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
