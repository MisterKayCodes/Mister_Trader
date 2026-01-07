import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Rule 11: Import handlers
from app.telegram.handlers.auth_handlers import cmd_start, cmd_signup, cmd_login
from app.telegram.handlers.menu_handlers import register_menu_handlers
from app.telegram.handlers import account_handlers

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Rule 1: Using MemoryStorage for session data
storage = MemoryStorage()
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=storage)

def register_all_handlers(dispatcher: Dispatcher):
    """Rule 11: Registration Registry."""
    # 1. Auth Handlers
    dispatcher.message.register(cmd_start, Command("start"))
    dispatcher.message.register(cmd_signup, Command("signup"))
    dispatcher.message.register(cmd_login, Command("login"))
    
    # 2. Account Handlers (Router includes FSM logic)
    dispatcher.include_router(account_handlers.router)
    
    # 3. Menu Handlers
    register_menu_handlers(dispatcher)

async def main():
    register_all_handlers(dp)
    logger.info("--- MisterTrader Bot Online (Persistent State Mode) ---")
    
    try:
        # Rule 13: Defaulting to MarkdownV2
        await dp.start_polling(bot, default=dict(parse_mode="MarkdownV2"))
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
