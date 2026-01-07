from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class TradeMediaBase(BaseModel):
    trade_id: int = Field(..., description="ID of the trade this media belongs to")
    type: str = Field(..., min_length=1, max_length=50, description="Type: ENTRY_SCREENSHOT, EXIT_SCREENSHOT")
    file_path: str = Field(..., min_length=1, description="Path to the media file")

class TradeMediaCreate(TradeMediaBase):
    # Rule 14: user_id is NOT here because we get it from the JWT Badge.
    pass

class TradeMediaUpdate(BaseModel):
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    file_path: Optional[str] = Field(None, min_length=1)

class TradeMediaRead(TradeMediaBase):
    id: int
    user_id: int # Rule 1: Explicitly show ownership in the read state
    timestamp: datetime 

    # Rule 13: 2026 Pydantic V2 config (Fixes orm_mode warning)
    model_config = ConfigDict(from_attributes=True)
