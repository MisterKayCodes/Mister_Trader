from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# Rule 3: Single responsibility - Explicitly named for TradeMedia
class TradeMediaBase(BaseModel):
    trade_id: int = Field(..., description="ID of the trade this media belongs to")
    # Rule 13: In 2026/Pydantic V2, use Field(max_length=50) instead of constr
    type: str = Field(..., min_length=1, max_length=50, description="Type of media, e.g. 'Entry' or 'Exit'")
    file_path: str = Field(..., min_length=1, description="Path to the media file stored on disk")

class TradeMediaCreate(TradeMediaBase):
    """Rule 1: Explicitly named to match the import in your router."""
    pass

class TradeMediaUpdate(BaseModel):
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    file_path: Optional[str] = Field(None, min_length=1)

class TradeMediaRead(TradeMediaBase):
    id: int
    # Rule 13: Use 'timestamp' if your model uses 'timestamp', or 'created_at' if it uses that.
    # Based on your model:
    timestamp: datetime 

    # Rule 13: FIXES THE "orm_mode" WARNING
    model_config = ConfigDict(from_attributes=True)
