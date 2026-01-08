import os
import httpx
import logging
from aiogram import Router, F, types, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

@router.callback_query(F.data == "media_view")
async def list_trade_media(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth = user_data.get("access_token")
    acc_id = user_data.get("active_account_id")
    
    if not auth or not acc_id:
        return await callback.answer("❌ Session missing or no active vault.", show_alert=True)
        
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/trade-media?account_id={acc_id}",
                headers={"Authorization": f"Bearer {auth}"}
            )
            if resp.status_code == 200:
                media_list = resp.json()
                if not media_list:
                    return await callback.message.answer("No media found for this vault.")
                    
                for item in media_list[:5]: # Limit to avoid flooding
                    path = item.get("file_path", "").lstrip("/")
                    file_resp = await client.get(f"{BOT_BACKEND_URL}/{path}", headers={"Authorization": f"Bearer {auth}"})
                    if file_resp.status_code == 200:
                        photo = BufferedInputFile(file_resp.content, filename=os.path.basename(path))
                        await callback.message.answer_photo(photo, caption=f"Trade Media #{item['id']}")
            else:
                await callback.answer("❌ Failed to fetch media.", show_alert=True)
    except Exception as e:
        logger.error(f"Media view error: {e}")
        await callback.answer("❌ Connection error.")
    await callback.answer()
