from pydantic import BaseModel

class TelegramLogin(BaseModel):
    telegram_user_id: int
