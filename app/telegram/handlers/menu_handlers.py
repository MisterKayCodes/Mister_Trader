import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram.keyboards import reply_keyboards as rk
from app.telegram.keyboards import inline_keyboards as ik

logger = logging.getLogger(__name__)
router = Router()

# --- GLOBAL UTILITY HANDLERS ---

async def handle_cancel_action(message: Message, state: FSMContext):
    """
    Rule 7: Global cancel handler.
    Clears any active FSM state without logging the user out.
    """
    current_state = await state.get_state()
    if current_state is None:
        # If no state is active, just ensure the main menu is shown
        return await message.answer(
            "🏠 <b>Main Menu</b>", 
            reply_markup=rk.get_main_menu(), 
            parse_mode="HTML"
        )

    # Reset state to exit any forms (Accounts/Trades), but keep data (JWT)
    await state.set_state(None)
    await message.answer(
        "❌ <b>Action Cancelled.</b>\nReturned to main menu.",
        reply_markup=rk.get_main_menu(),
        parse_mode="HTML"
    )

# --- REPLY KEYBOARD HANDLERS (Main Categories) ---

async def handle_accounts_menu(message: Message):
    """Maps to /api/v1/accounts"""
    await message.answer(
        "📁 <b>Vault & Account Management</b>\n"
        "Manage your different trading accounts and switch your active context.",
        reply_markup=ik.get_account_options(),
        parse_mode="HTML"
    )

async def handle_trades_menu(message: Message):
    """Maps to /api/v1/trades"""
    await message.answer(
        "📊 <b>Trade Management</b>\n"
        "Monitor active positions or log new entries in your journal.",
        reply_markup=ik.get_trade_management(),
        parse_mode="HTML"
    )

async def handle_psychology_menu(message: Message):
    """Maps to /api/v1/trade-psychology"""
    await message.answer(
        "🧠 <b>Psychology & Discipline</b>\n"
        "Review your emotional state and plan adherence stats.",
        reply_markup=ik.get_psychology_tools(),
        parse_mode="HTML"
    )

async def handle_media_menu(message: Message):
    """Maps to /api/v1/trade-media"""
    await message.answer(
        "🖼️ <b>Trade Media</b>\n"
        "View and upload screenshots of your setups and executions.",
        reply_markup=ik.get_media_options(),
        parse_mode="HTML"
    )

async def handle_activity_menu(message: Message):
    """Maps to /api/v1/activities"""
    await message.answer(
        "📈 <b>System Activity</b>\n"
        "Review your recent logs and system interactions.",
        reply_markup=ik.get_activity_log(),
        parse_mode="HTML"
    )

async def handle_back_to_main(message: Message):
    """Rule 7: Graceful recovery to home state."""
    await message.answer(
        "🔙 <b>Returned to Main Menu</b>",
        reply_markup=rk.get_main_menu(),
        parse_mode="HTML"
    )

# --- INLINE CALLBACK HANDLERS (Generic Actions) ---

async def handle_menu_callback(callback: CallbackQuery):
    """
    Handles 'Back' or 'Main Menu' inline requests.
    Rule 13: Consistent navigation.
    """
    if callback.data == "menu_main":
        await callback.message.edit_text(
            "🏠 <b>Main Menu</b>\nSelect a category from the bottom keyboard.",
            parse_mode="HTML"
        )
    await callback.answer()

# --- REGISTRATION FUNCTION ---

def register_menu_handlers(dp):
    """Rule 1: Known State - Centralized registration."""
    
    # 1. Global Cancel Filter (Highest Priority)
    dp.message.register(handle_cancel_action, F.text == "❌ Cancel")
    
    # 2. Main Menu Text Filters
    dp.message.register(handle_accounts_menu, F.text == "📁 Accounts")
    dp.message.register(handle_trades_menu, F.text == "📊 Active Trades")
    dp.message.register(handle_psychology_menu, F.text == "🧠 Psychology")
    dp.message.register(handle_media_menu, F.text == "🖼️ Trade Media")
    dp.message.register(handle_activity_menu, F.text == "📈 Activity")
    
    # 3. Navigation Filters
    dp.message.register(handle_back_to_main, F.text == "🔙 Back to Main Menu")
    
    # 4. Global Callback for 'Back' buttons in Inline Keyboards
    dp.callback_query.register(handle_menu_callback, F.data == "menu_main")
