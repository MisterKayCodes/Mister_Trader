from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    telegram_user_id: int

class UserRead(BaseModel):
    id: int
    telegram_user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
