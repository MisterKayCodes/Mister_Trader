from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ActivityBase(BaseModel):
    user_id: int
    date: date
    activity_type: str


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
