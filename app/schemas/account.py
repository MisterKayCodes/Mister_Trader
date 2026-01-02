from pydantic import BaseModel
from datetime import datetime

class AccountBase(BaseModel):
    name: str

class AccountCreate(AccountBase):
    user_id: int  # The owner of the account

class AccountRead(AccountBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AccountUpdate(AccountBase):
    pass
