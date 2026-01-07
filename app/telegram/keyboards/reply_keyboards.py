from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """
    Rule 13: Consistent UI layout.
    Maps to: Accounts, Trades, Psychology, and Media routers.
    """
    keyboard = [
        [KeyboardButton(text="📁 Accounts"), KeyboardButton(text="📊 Active Trades")],
        [KeyboardButton(text="🧠 Psychology"), KeyboardButton(text="🎙️ Voice Notes")],
        [KeyboardButton(text="🖼️ Trade Media"), KeyboardButton(text="📈 Activity")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Select a category..."
    )
