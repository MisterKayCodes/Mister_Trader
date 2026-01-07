import os
import httpx
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.telegram.states.account_states import AccountStates
from app.telegram.keyboards.reply_keyboards import get_main_menu

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

@router.message(AccountStates.waiting_for_name)
async def process_account_creation(message: Message, state: FSMContext):
    """
    Rule 14: Uses the stored JWT token to create an account.
    """
    vault_name = message.text.strip()
    
    # 1. RETRIEVE the access_token we saved during login
    user_data = await state.get_data()
    auth_token = user_data.get("access_token")

    # If the token is missing, the user timed out or didn't login properly
    if not auth_token:
        await state.clear()
        return await message.answer("❌ Session expired. Please /login again.")

    async with httpx.AsyncClient() as client:
        try:
            # 2. POST to /api/v1/accounts (No trailing slash to avoid 307)
            # 3. Include the Token in the Authorization Header
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/accounts", 
                json={"name": vault_name},
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )

            if response.status_code == 201:
                # Rule 6: Success - Clear the 'waiting' state and show menu
                await state.clear()
                # We keep the token in the 'permanent' state if we want, 
                # but for now, we clear FSM to finish the creation flow.
                await message.answer(
                    f"🎊 *Vault '{vault_name}' Created\!*\n\n"
                    f"Active Vault: `{vault_name}`",
                    reply_markup=get_main_menu()
                )
            else:
                logger.error(f"Vault creation failed: {response.text}")
                await message.answer("❌ Failed to create vault. Try a different name.")
        
        except Exception as e:
            logger.error(f"Connection error during vault creation: {e}")
            await message.answer("🔌 Backend unreachable.")
