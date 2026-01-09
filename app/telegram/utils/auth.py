from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from typing import Optional, Tuple
import httpx
import os

BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")


async def get_auth_token(state: FSMContext) -> Optional[str]:
    """Get access token from FSM state."""
    data = await state.get_data() or {}
    return data.get("access_token")


async def get_user_id_from_state(state: FSMContext) -> Optional[int]:
    """Get user_id by fetching from backend using the stored access token."""
    token = await get_auth_token(state)
    if not token:
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get("id")
    except Exception:
        pass
    return None


async def is_authenticated(state: FSMContext) -> bool:
    """Check if user has a valid access token."""
    data = await state.get_data() or {}
    return bool(data.get("access_token"))


async def check_auth(state: FSMContext) -> Tuple[bool, Optional[str]]:
    """Check authentication and return (is_authenticated, access_token)."""
    data = await state.get_data() or {}
    token = data.get("access_token")
    return (bool(token), token)
