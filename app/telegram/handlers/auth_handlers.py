import logging
import httpx
import os
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.telegram.states.account_states import AccountStates
from app.telegram.keyboards.reply_keyboards import get_main_menu

# Rule 11: Backend integration settings
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
logger = logging.getLogger(__name__)

async def cmd_start(message: Message, state: FSMContext):
    """
    Rule 6: Check for existing session. Redirect to menu if token exists.
    Using HTML mode for cleaner 2026 formatting.
    """
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")

    if auth_token:
        await message.answer(
            "👋 <b>Welcome back to Mister Trader!</b>\n\n"
            "Your session is active. Use the menu below to manage your journal.",
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "🚀 <b>Welcome to Mister Trader</b>\n\n"
            "1. <code>/signup 1234</code> - Create your account\n"
            "2. <code>/login 1234</code> - Access your dashboard",
            parse_mode="HTML"
        )

async def cmd_signup(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❌ <b>Format Error:</b> Use <code>/signup 1234</code>", parse_mode="HTML")

    pin = parts[1]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/users/signup", 
                json={"telegram_user_id": user_id, "pin": pin},
                timeout=10.0
            )
            
            if response.status_code == 201:
                await message.answer("✅ <b>Registration successful!</b>\nUse <code>/login 1234</code> to start.", parse_mode="HTML")
            elif response.status_code == 400:
                await message.answer("ℹ️ <b>Already registered.</b>", parse_mode="HTML")
            else:
                await message.answer("❌ <b>Registration failed.</b>", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Signup error: {e}")
            await message.answer("🔌 <b>Backend unreachable.</b>", parse_mode="HTML")

async def cmd_login(message: Message, state: FSMContext):
    user_id = message.from_user.id
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❌ <b>Format Error:</b> Use <code>/login 1234</code>", parse_mode="HTML")

    pin = parts[1]

    async with httpx.AsyncClient() as client:
        try:
            login_resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/users/login", 
                json={"telegram_user_id": user_id, "pin": pin},
                timeout=10.0
            )

            if login_resp.status_code == 200:
                token_data = login_resp.json()
                access_token = token_data.get("access_token")

                # Step 1: Fetch accounts to identify the active one
                acc_resp = await client.get(
                    f"{BOT_BACKEND_URL}/api/v1/accounts",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10.0
                )
                
                if acc_resp.status_code == 200:
                    accounts = acc_resp.json()
                    
                    if not accounts:
                        # Save only token, wait for user to create account name
                        await state.update_data(access_token=access_token)
                        await message.answer(
                            "✅ <b>Login successful!</b>\n\n"
                            "You don't have a vault yet. Please enter a <b>Name</b> for your first account (e.g. Personal):",
                            parse_mode="HTML"
                        )
                        await state.set_state(AccountStates.waiting_for_name)
                    else:
                        # FIX: Extract the first account and save its ID to state
                        # This prevents 'account_id=None' errors in Voice Handlers
                        first_account = accounts[0] if isinstance(accounts, list) else accounts
                        active_name = first_account.get('name')
                        active_id = first_account.get('id')

                        await state.update_data(
                            access_token=access_token,
                            active_account_id=active_id
                        )

                        await message.answer(
                            f"✅ <b>Login successful!</b>\n\n"
                            f"<b>Active Vault:</b> <code>{active_name}</code>",
                            reply_markup=get_main_menu(),
                            parse_mode="HTML"
                        )
                else:
                    await state.update_data(access_token=access_token)
                    await message.answer("✅ <b>Login successful!</b>\nEnter a name for your first vault:", parse_mode="HTML")
                    await state.set_state(AccountStates.waiting_for_name)
            
            elif login_resp.status_code == 401:
                await message.answer("❌ <b>Invalid PIN.</b> Access denied.", parse_mode="HTML")
            else:
                await message.answer("⚠️ <b>System error during login.</b>", parse_mode="HTML")
                
        except Exception as e:
            logger.error(f"Login failure: {e}")
            await message.answer("🔌 <b>Connection failure.</b>", parse_mode="HTML")
