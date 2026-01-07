import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.telegram.keyboards import reply_keyboards as rk
from app.telegram.keyboards import inline_keyboards as ik

logger = logging.getLogger(__name__)
router = Router()

# --- REPLY KEYBOARD HANDLERS (Main Categories) ---

async def handle_accounts_menu(message: Message):
    """Maps to /api/v1/accounts"""
    await message.answer(
        "📁 *Vault & Account Management*\n"
        "Manage your different trading accounts and switch your active context\.",
        reply_markup=ik.get_account_options()
    )

async def handle_trades_menu(message: Message):
    """Maps to /api/v1/trades"""
    await message.answer(
        "📊 *Trade Management*\n"
        "Monitor active positions or log new entries in your journal\.",
        reply_markup=ik.get_trade_management()
    )

async def handle_psychology_menu(message: Message):
    """Maps to /api/v1/trade-psychology"""
    await message.answer(
        "🧠 *Psychology & Discipline*\n"
        "Review your emotional state and plan adherence stats\.",
        reply_markup=ik.get_psychology_tools()
    )

async def handle_media_menu(message: Message):
    """Maps to /api/v1/trade-media"""
    await message.answer(
        "🖼️ *Trade Media*\n"
        "View and upload screenshots of your setups and executions\.",
        reply_markup=ik.get_media_options()
    )

async def handle_activity_menu(message: Message):
    """Maps to /api/v1/activities"""
    await message.answer(
        "📈 *System Activity*\n"
        "Review your recent logs and system interactions\.",
        reply_markup=ik.get_activity_log()
    )

async def handle_back_to_main(message: Message):
    """Rule 7: Graceful recovery to home state."""
    await message.answer(
        "🔙 *Returned to Main Menu*",
        reply_markup=rk.get_main_menu()
    )

# --- INLINE CALLBACK HANDLERS (Generic Actions) ---

async def handle_menu_callback(callback: CallbackQuery):
    """
    Handles 'Back' or 'Main Menu' inline requests.
    Rule 13: Consistent navigation.
    """
    if callback.data == "menu_main":
        await callback.message.edit_text(
            "🏠 *Main Menu*\nSelect a category from the bottom keyboard\."
        )
    await callback.answer()

# --- REGISTRATION FUNCTION ---

def register_menu_handlers(dp):
    """Rule 1: Known State - Centralized registration."""
    # Main Menu Text Filters
    dp.message.register(handle_accounts_menu, F.text == "📁 Accounts")
    dp.message.register(handle_trades_menu, F.text == "📊 Active Trades")
    dp.message.register(handle_psychology_menu, F.text == "🧠 Psychology")
    dp.message.register(handle_media_menu, F.text == "🖼️ Trade Media")
    dp.message.register(handle_activity_menu, F.text == "📈 Activity")
    
    # Navigation Filters
    dp.message.register(handle_back_to_main, F.text == "🔙 Back to Main Menu")
    
    # Global Callback for 'Back' buttons in Inline Keyboards
    dp.callback_query.register(handle_menu_callback, F.data == "menu_main")
