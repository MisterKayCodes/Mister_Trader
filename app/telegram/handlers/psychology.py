import os
import httpx
import logging
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.telegram.keyboards import inline_keyboards as ik
from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

@router.callback_query(F.data == "psych_stats")
async def show_psychology_stats(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth = user_data.get("access_token")
    acc_id = user_data.get("active_account_id")
    
    if not auth or not acc_id:
        return await callback.answer("❌ Session missing or no active vault.", show_alert=True)
        
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/trade-psychology/stats?account_id={acc_id}",
                headers={"Authorization": f"Bearer {auth}"}
            )
            if resp.status_code == 200:
                stats = resp.json()
                msg = (
                    "🧠 <b>Psychology Stats</b>\n\n"
                    f"Plan Adherence: <code>{stats.get('plan_adherence', 0)}%</code>\n"
                    f"Emotional Stability: <code>{stats.get('emotional_stability', 'N/A')}</code>\n"
                    f"Top Mistake: <code>{stats.get('common_mistake', 'None')}</code>"
                )
                await callback.message.answer(msg, parse_mode="HTML")
            else:
                await callback.answer("❌ Failed to fetch stats.", show_alert=True)
    except Exception as e:
        logger.error(f"Psychology stats error: {e}")
        await callback.answer("❌ Connection error.")
    await callback.answer()
