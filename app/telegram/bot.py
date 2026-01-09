import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from dotenv import load_dotenv

from app.telegram.handlers.auth_handlers import cmd_start, cmd_signup, cmd_login
from app.telegram.handlers.menu_handlers import register_menu_handlers
from app.telegram.handlers import (
    account_handlers,
    trade_handlers,
    voice_handlers,
    psychology_handlers,
    media_handlers,
    activity_handlers,
    stats_handlers,
    export_handlers,
    strategy_handlers,
    plan_handlers
)
from app.telegram.scheduler import setup_scheduler

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

storage = SQLStorage(db_path="fsm_storage.db")
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=storage)

def register_all_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(cmd_start, Command("start"))
    dispatcher.message.register(cmd_signup, Command("signup"))
    dispatcher.message.register(cmd_login, Command("login"))
    
    dispatcher.include_router(account_handlers.router)
    dispatcher.include_router(trade_handlers.router)
    dispatcher.include_router(voice_handlers.router)
    dispatcher.include_router(psychology_handlers.router)
    dispatcher.include_router(media_handlers.router)
    dispatcher.include_router(activity_handlers.router)
    dispatcher.include_router(stats_handlers.router)
    dispatcher.include_router(export_handlers.router)
    dispatcher.include_router(strategy_handlers.router)
    dispatcher.include_router(plan_handlers.router)
    
    register_menu_handlers(dispatcher)

async def main():
    register_all_handlers(dp)
    
    scheduler = None
    try:
        scheduler = setup_scheduler(bot)
        scheduler.start()
        logger.info("Weekly summary scheduler started (Sundays at 20:00 UTC)")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
    
    logger.info("--- MisterTrader Bot Online (HTML Mode 2026) ---")
    
    try:
        await dp.start_polling(bot, default=dict(parse_mode="HTML"))
    finally:
        if scheduler:
            try:
                scheduler.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down scheduler: {e}")
        await bot.session.close()
        await storage.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")
