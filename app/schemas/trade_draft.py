from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class TradeDraftBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    side: str = Field(..., pattern="^(BUY|SELL)$")
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None

class TradeDraftCreate(TradeDraftBase):
    account_id: int

class TradeDraftRead(TradeDraftBase):
    id: int
    account_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TradeDraftUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
