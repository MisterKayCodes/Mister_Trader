from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class ActivityBase(BaseModel):
    date: date
    activity_type: str

class ActivityCreate(ActivityBase):
    # Rule 14: user_id is REMOVED from here. 
    # We never trust the client to tell us who they are.
    pass

class ActivityRead(ActivityBase):
    id: int
    user_id: int
    created_at: Optional[datetime]

    # Rule 13: 2026 Pydantic V2 Config
    model_config = ConfigDict(from_attributes=True)
