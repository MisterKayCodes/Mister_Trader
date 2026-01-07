import logging
import asyncio
import httpx
import os
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Rule 11: Bot is an external integration; it needs to know where the backend lives
load_dotenv()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup logging (Rule 10: Observability)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rule 1: Use verified local env for bot state
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Rule 6: Explicit commands only
    await message.answer(
        "Welcome to Mister_Trader!\n\n"
        "To register, please use the /signup command followed by a 4-digit PIN.\n"
        "Example: `/signup 1234`",
        parse_mode="Markdown"
    )

@dp.message(Command("signup"))
async def cmd_signup(message: Message):
    user_id = message.from_user.id
    command_args = message.text.split()

    # Rule 4: Explicit check for PIN format
    if len(command_args) != 2 or not command_args[1].isdigit():
        return await message.answer("❌ Invalid format. Use: `/signup 1234`")

    pin = command_args[1]
    user_data = {"telegram_user_id": user_id, "pin": pin}

    async with httpx.AsyncClient() as client:
        try:
            # Rule 13: Pointing to the new Phase 1 Auth endpoint
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/users/signup", 
                json=user_data,
                timeout=10.0
            )

            if response.status_code == 201:
                await message.answer("✅ Registration successful! You can now log in.")
            elif response.status_code == 400:
                await message.answer("ℹ️ You are already registered.")
            else:
                logger.error(f"Backend Error {response.status_code}")
                await message.answer("❌ Registration failed. System error.")

        except httpx.RequestError as e:
            # Rule 7: Design for recovery if backend is down
            logger.error(f"Connection Failure: {e}")
            await message.answer("🔌 Could not connect to the backend server.")

async def main():
    logger.info("--- Starting Telegram Bot (Auth Mode 2026) ---")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
