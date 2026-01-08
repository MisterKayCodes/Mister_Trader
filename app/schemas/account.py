from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AccountBase(BaseModel):
    name: str

class AccountCreate(AccountBase):
    # Rule 14: user_id is REMOVED here. 
    # The user should never send their own ID in the body; 
    # we get it from the JWT Token.
    pass

class AccountRead(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    # Rule 13: 2026 Pydantic V2 config
    model_config = ConfigDict(from_attributes=True)
