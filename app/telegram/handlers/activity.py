import os
import httpx
import logging
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

@router.callback_query(F.data == "activity_view")
async def show_recent_activity(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth = user_data.get("access_token")
    
    if not auth:
        return await callback.answer("❌ Session missing.", show_alert=True)
        
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/activities",
                headers={"Authorization": f"Bearer {auth}"}
            )
            if resp.status_code == 200:
                activities = resp.json()
                if not activities:
                    return await callback.message.answer("No recent activity found.")
                    
                msg = "📈 <b>Recent Activity</b>\n\n"
                for act in activities[:10]:
                    msg += f"• {act.get('description', 'Action')} - <code>{act.get('timestamp', '').split('T')[0]}</code>\n"
                await callback.message.answer(msg, parse_mode="HTML")
            else:
                await callback.answer("❌ Failed to fetch activity.", show_alert=True)
    except Exception as e:
        logger.error(f"Activity view error: {e}")
        await callback.answer("❌ Connection error.")
    await callback.answer()
