import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
# Rule 1: Updated to SQLStorage for session persistence across restarts
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from dotenv import load_dotenv

# Rule 11: Import handlers
from app.telegram.handlers.auth_handlers import cmd_start, cmd_signup, cmd_login
from app.telegram.handlers.menu_handlers import register_menu_handlers
from app.telegram.handlers import account_handlers

load_dotenv()

# Rule 10: Standardized 2026 Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Rule 1: Using SQLStorage to persist session data (access_tokens)
storage = SQLStorage(db_path="fsm_storage.db")
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=storage)

def register_all_handlers(dispatcher: Dispatcher):
    """Rule 11: Centralized handler registration."""
    # 1. Auth Handlers
    dispatcher.message.register(cmd_start, Command("start"))
    dispatcher.message.register(cmd_signup, Command("signup"))
    dispatcher.message.register(cmd_login, Command("login"))
    
    # 2. Account/Vault Handlers (FSM Router)
    dispatcher.include_router(account_handlers.router)
    
    # 3. Menu Handlers
    register_menu_handlers(dispatcher)

async def main():
    register_all_handlers(dp)
    logger.info("--- MisterTrader Bot Online (HTML Mode 2026) ---")
    
    try:
        # Rule 13: Using HTML to solve formatting issues and remove visible slashes
        # Standard in 2026 for stable UI rendering
        await dp.start_polling(bot, default=dict(parse_mode="HTML"))
    finally:
        # Rule 7: Clean shutdown
        await bot.session.close()
        # Ensure SQLite connection is closed
        await storage.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")
