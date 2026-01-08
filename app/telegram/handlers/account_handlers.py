import os
import httpx
import logging
from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.telegram.states.account_states import AccountStates
from app.telegram.keyboards.reply_keyboards import get_main_menu
from app.telegram.keyboards.inline_keyboards import get_account_options

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# --- Main Menu Entry ---

@router.message(F.text == "📁 Accounts")
async def show_account_menu(message: Message, state: FSMContext):
    """
    Entry point for account management.
    Displays the currently active vault name from FSM data.
    """
    user_data = await state.get_data() or {}
    active_name = user_data.get("active_account_name", "None (Please Switch)")

    await message.answer(
        f"📁 <b>Vault Management</b>\n\n"
        f"<b>Active Vault:</b> <code>{active_name}</code>\n\n"
        f"Select an action below:",
        reply_markup=get_account_options(),
        parse_mode="HTML"
    )

# --- Create Account Flow ---

@router.callback_query(F.data == "account_create")
async def start_account_creation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Enter a name for your new Vault (e.g., 'Personal' or 'Trading'):")
    await state.set_state(AccountStates.waiting_for_name)
    await callback.answer()

@router.message(AccountStates.waiting_for_name)
async def process_account_creation(message: Message, state: FSMContext):
    vault_name = message.text.strip()
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")

    if not auth_token:
        return await message.answer("❌ Session expired. Please /login again.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/accounts", 
                json={"name": vault_name},
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )

            if response.status_code == 201:
                # Rule 6: Finish state but preserve data
                await state.set_state(None)
                
                # Automatically set as active if it's the first or newly created
                acc_data = response.json()
                await state.update_data(
                    active_account_id=str(acc_data['id']), 
                    active_account_name=acc_data['name']
                )

                await message.answer(
                    f"✅ <b>Vault '{vault_name}' Created and Set as Active!</b>",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = response.json().get("detail", "Failed to create vault")
                await message.answer(f"❌ <b>Error:</b> {detail}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Creation error: {e}")
            await message.answer("🔌 Backend unreachable.")

# --- Switch/Active Account Flow ---

@router.callback_query(F.data == "account_switch")
async def list_accounts_for_switch(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    current_active_id = str(user_data.get("active_account_id"))

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/accounts",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        if resp.status_code == 200:
            accounts = resp.json()
            if not accounts:
                return await callback.message.answer("You don't have any vaults yet.")

            buttons = []
            for acc in accounts:
                # Rule 13: UI Polish - Highlight current active vault
                is_active = str(acc['id']) == current_active_id
                label = f"✅ {acc['name']}" if is_active else f"📂 {acc['name']}"
                
                buttons.append([InlineKeyboardButton(
                    text=label, 
                    callback_data=f"switch_to_{acc['id']}_{acc['name']}"
                )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                "<b>Select the Vault to set as Active:</b>", 
                reply_markup=keyboard, 
                parse_mode="HTML"
            )
        else:
            await callback.answer("Failed to fetch accounts.")
    await callback.answer()

@router.callback_query(F.data.startswith("switch_to_"))
async def process_account_switch(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    acc_id = parts[2]
    acc_name = "_".join(parts[3:])

    # Update FSM data
    await state.update_data(active_account_id=acc_id, active_account_name=acc_name)
    
    # Refresh the menu to show the new active status
    await callback.message.edit_text(
        f"✅ <b>Active Vault switched to:</b> <code>{acc_name}</code>\n\n"
        f"Return to the menu using the buttons below.",
        reply_markup=get_account_options(),
        parse_mode="HTML"
    )
    await callback.answer(f"Switched to {acc_name}")

# --- Delete Account Flow ---

@router.callback_query(F.data == "account_delete")
async def list_accounts_for_deletion(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/accounts",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        if resp.status_code == 200:
            accounts = resp.json()
            if not accounts:
                return await callback.message.answer("No vaults available to delete.")

            buttons = []
            for acc in accounts:
                buttons.append([InlineKeyboardButton(
                    text=f"🗑️ Delete {acc['name']}", 
                    callback_data=f"confirm_delete_{acc['id']}"
                )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                "<b>⚠️ Select a Vault to PERMANENTLY delete:</b>", 
                reply_markup=keyboard, 
                parse_mode="HTML"
            )
        else:
            await callback.answer("Failed to fetch accounts.")
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete_"))
async def process_account_deletion(callback: types.CallbackQuery, state: FSMContext):
    acc_id = callback.data.split("_")[2]
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{BOT_BACKEND_URL}/api/v1/accounts/{acc_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )

            if response.status_code == 204:
                # If deleted account was active, clear it
                if str(user_data.get("active_account_id")) == str(acc_id):
                    await state.update_data(active_account_id=None, active_account_name=None)
                
                await callback.message.edit_text(
                    "✅ <b>Vault deleted successfully.</b>", 
                    reply_markup=get_account_options(),
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer("❌ Could not delete vault (Unauthorized or Not Found).")
        except Exception as e:
            logger.error(f"Delete error: {e}")
            await callback.answer("🔌 Backend error.")
    await callback.answer()
