import logging
from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from app.core.database import SessionLocal
from app.services.export_service import export_trades_to_csv, get_export_filename
from app.telegram.utils.auth import get_user_id_from_state

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("export"))
async def cmd_export(message: Message, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await message.answer("Please /login first.")
        return
    
    await message.answer("Generating your trade export...")
    
    db = SessionLocal()
    try:
        csv_data = export_trades_to_csv(db, user_id)
        filename = get_export_filename(user_id)
        
        file = BufferedInputFile(csv_data.read(), filename=filename)
        
        await message.answer_document(
            document=file,
            caption="Here's your complete trade history in CSV format. You can open this in Excel or Google Sheets."
        )
    except Exception as e:
        logger.error(f"Export failed: {e}")
        await message.answer("Failed to generate export. Please try again.")
    finally:
        db.close()
