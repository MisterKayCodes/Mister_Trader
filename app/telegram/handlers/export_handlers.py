import os
import httpx
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router()
<<<<<<< HEAD
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
=======
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:5000")
>>>>>>> 9e6925a (Syncing latest local changes for deployment)


@router.message(F.text == "📥 Export")
async def menu_export(message: Message, state: FSMContext):
    await cmd_export(message, state)


@router.message(Command("export"))
async def cmd_export(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await message.answer("Please /login first.")
        return
    
    await message.answer("Generating your trade export...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/export/trades/csv",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=30.0
            )
            response.raise_for_status()
            
            filename = response.headers.get("content-disposition", "trades.csv")
            if "filename=" in filename:
                filename = filename.split("filename=")[1].strip('"')
            else:
                filename = "trades_export.csv"
            
            file = BufferedInputFile(response.content, filename=filename)
            
            await message.answer_document(
                document=file,
                caption="Here's your complete trade history in CSV format. You can open this in Excel or Google Sheets."
            )
    except Exception as e:
        logger.error(f"Export failed: {e}")
        await message.answer("Failed to generate export. Please try again.")


@router.callback_query(F.data == "export:all")
async def cb_export_all(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    await callback.answer("Generating export...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/export/trades/csv",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=30.0
            )
            response.raise_for_status()
            
            filename = response.headers.get("content-disposition", "trades.csv")
            if "filename=" in filename:
                filename = filename.split("filename=")[1].strip('"')
            else:
                filename = "trades_export.csv"
            
            file = BufferedInputFile(response.content, filename=filename)
            
            await callback.message.answer_document(
                document=file,
                caption="Here's your complete trade history in CSV format. You can open this in Excel or Google Sheets."
            )
    except Exception as e:
        logger.error(f"Export failed: {e}")
        await callback.message.answer("Failed to generate export. Please try again.")
