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
    """
    user_data = await state.get_data()
    auth_token = user_data.get("access_token")

    if auth_token:
        await message.answer(
            "👋 *Welcome back to Mister\_Trader\!*\n"
            "Your session is active\. Use the menu below\.",
            reply_markup=get_main_menu()
        )
    else:
        # MarkdownV2 requires escaping dots and dashes
        await message.answer(
            "Welcome to Mister\_Trader\!\n\n"
            "1\. `/signup 1234` \- Create your account\n"
            "2\. `/login 1234` \- Access your dashboard"
        )

async def cmd_signup(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❌ Format: ` /signup 1234 `")

    pin = parts[1]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/users/signup", 
                json={"telegram_user_id": user_id, "pin": pin},
                timeout=10.0
            )
            
            if response.status_code == 201:
                await message.answer("✅ Registration successful\! Use `/login` to start\.")
            elif response.status_code == 400:
                await message.answer("ℹ️ You are already registered\.")
            else:
                await message.answer("❌ Registration failed\.")
        except Exception as e:
            logger.error(f"Signup error: {e}")
            await message.answer("🔌 Backend unreachable\.")

async def cmd_login(message: Message, state: FSMContext):
    """Rule 14: JWT Auth + Rule 1: Save session state."""
    user_id = message.from_user.id
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❌ Format: ` /login 1234 `")

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

                # Save token in FSM state
                await state.update_data(access_token=access_token)

                # Check for accounts
                acc_resp = await client.get(
                    f"{BOT_BACKEND_URL}/api/v1/accounts",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10.0
                )
                
                if acc_resp.status_code == 200:
                    accounts = acc_resp.json()
                    
                    if not accounts or (isinstance(accounts, list) and len(accounts) == 0):
                        await message.answer(
                            "✅ *Login successful\!*\n\n"
                            "You don't have a vault yet\. Enter a **Name** for your first account:"
                        )
                        await state.set_state(AccountStates.waiting_for_name)
                    else:
                        active_name = accounts[0]['name'] if isinstance(accounts, list) else accounts.get('name')
                        await message.answer(
                            f"✅ *Login successful\!*\nActive Vault: `{active_name}`",
                            reply_markup=get_main_menu()
                        )
                else:
                    await message.answer("✅ *Login successful\!*\nEnter a **Name** for your first vault:")
                    await state.set_state(AccountStates.waiting_for_name)
            
            elif login_resp.status_code == 401:
                await message.answer("❌ Invalid PIN\. Access denied\.")
            else:
                await message.answer("⚠️ System error during login\.")
                
        except Exception as e:
            logger.error(f"Login failure: {e}")
            await message.answer("🔌 Connection failure\.")
