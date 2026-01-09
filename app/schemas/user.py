from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    telegram_user_id: int

class UserCreate(UserBase):
    # Rule 14: PIN is required for signup/login but never returned in Read
    pin: str 

class UserRead(UserBase):
    id: int
    created_at: datetime
    # Rule 13: Using 2026 Pydantic V2 config (fixes UserWarnings)
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
