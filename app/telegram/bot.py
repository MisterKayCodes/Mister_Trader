import os
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
import httpx
import asyncio

# Load environment variables from .env
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} started the bot")

    # Prepare data to send to backend API
    user_data = {"telegram_user_id": user_id}

    async with httpx.AsyncClient() as client:
        try:
            # Try to create user via POST /api/v1/users/
            response = await client.post(f"{BACKEND_API_URL}/api/v1/users/", json=user_data)

            if response.status_code == 400:
                # User already exists - fetch their data via GET /api/v1/users/{id}
                # Since we only have telegram_user_id, you might want an endpoint to get user by telegram_user_id,
                # but for simplicity here we just inform user already registered.
                await message.answer("You are already registered in the system!")
            elif response.status_code == 200 or response.status_code == 201:
                user_info = response.json()
                await message.answer(f"Welcome! Your user ID {user_info['id']} has been registered.")
            else:
                logger.error(f"Unexpected response {response.status_code}: {response.text}")
                await message.answer("Sorry, something went wrong with registration. Please try again later.")
        except httpx.RequestError as e:
            logger.error(f"Error connecting to backend API: {e}")
            await message.answer("Could not connect to the backend server. Please try again later.")


async def main():
    try:
        logger.info("Starting Telegram bot...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
