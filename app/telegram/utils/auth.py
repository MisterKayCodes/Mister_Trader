from aiogram.fsm.context import FSMContext
from typing import Optional
from jose import jwt, JWTError

from app.core.config import settings
from app.core.database import SessionLocal
from app.services import auth_service


async def get_auth_token(state: FSMContext) -> Optional[str]:
    """Get access token from FSM state."""
    data = await state.get_data() or {}
    return data.get("access_token")


async def get_user_id_from_state(state: FSMContext) -> Optional[int]:
    """
    Get user_id by decoding the JWT token stored in state.
    Returns the database user.id (not telegram_user_id).
    """
    token = await get_auth_token(state)
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telegram_user_id_str = payload.get("sub")
        if not telegram_user_id_str:
            return None
        
        telegram_user_id = int(telegram_user_id_str)
        
        db = SessionLocal()
        try:
            user = auth_service.get_user_by_telegram_id(db, telegram_user_id)
            if user:
                return user.id
        finally:
            db.close()
    except (JWTError, ValueError):
        pass
    
    return None


async def is_authenticated(state: FSMContext) -> bool:
    """Check if user has a valid access token."""
    data = await state.get_data() or {}
    return bool(data.get("access_token"))
