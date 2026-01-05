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
    updated_at: datetime  # Include updated_at here for output

    class Config:
        orm_mode = True

class TradeDraftUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
