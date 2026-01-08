from aiogram.fsm.context import FSMContext
from typing import Optional


async def get_user_id_from_state(state: FSMContext) -> Optional[int]:
    data = await state.get_data() or {}
    return data.get("user_id")


async def get_auth_token_from_state(state: FSMContext) -> Optional[str]:
    data = await state.get_data() or {}
    return data.get("access_token")


async def is_authenticated(state: FSMContext) -> bool:
    data = await state.get_data() or {}
    return bool(data.get("user_id") and data.get("access_token"))
