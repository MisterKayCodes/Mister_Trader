from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
# Rule 11: Import logic/types from the model layer
from app.models.trade_psychology import DisciplineLevel, ConfidenceLevel

class TradePsychologyBase(BaseModel):
    """Rule 4: Explicit and readable base attributes."""
    trade_id: int
    discipline: DisciplineLevel
    confidence: ConfidenceLevel
    followed_plan: bool
    notes: Optional[str] = Field(None, description="The 'Why' behind the trade (Rule 17)")

class TradePsychologyCreate(TradePsychologyBase):
    """Schema for creation - matches base."""
    pass

class TradePsychologyRead(TradePsychologyBase):
    """Rule 13: Uses model_config for Pydantic V2 compatibility."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TradePsychologyUpdate(BaseModel):
    """Rule 1: Partial updates for flexible state management."""
    discipline: Optional[DisciplineLevel] = None
    confidence: Optional[ConfidenceLevel] = None
    followed_plan: Optional[bool] = None
    notes: Optional[str] = None
