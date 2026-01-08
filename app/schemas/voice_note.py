from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TradeState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class VoiceNoteBase(BaseModel):
    trade_id: int
    file_path: str
    trade_state_at_time: TradeState

class VoiceNoteCreate(VoiceNoteBase):
    pass

class VoiceNoteUpdate(BaseModel):
    file_path: str | None = None
    trade_state_at_time: TradeState | None = None

class VoiceNoteRead(VoiceNoteBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True  # Use for Pydantic v2 compatibility with ORM mode
