from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Rule 4: Explicit and readable base attributes
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
    # Rule 1: Remove user_id here. The backend now gets it from the JWT badge.

class TradeRead(TradeBase):
    id: int
    account_id: int
    user_id: int # Rule 1: No longer optional in the model or read schema
    created_at: datetime
    updated_at: datetime

    # Rule 13: Standard 2026 Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)

class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    state: Optional[str] = None
    open_timestamp: Optional[datetime] = None
    close_timestamp: Optional[datetime] = None
    # Rule 13: Standard 2026 Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)
    
# Note: No user_id or account_id in update schema to prevent unauthorized changes.