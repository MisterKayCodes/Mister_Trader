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

def get_back_to_main_menu():
    """Provides a button to return to the main menu."""
    keyboard = [
        [KeyboardButton(text="🔙 Back to Main Menu")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Return to the main menu..."
    )

def get_cancel_action():
    """Provides a button to cancel the current action."""
    keyboard = [
        [KeyboardButton(text="❌ Cancel")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Cancel the current action..."
    )

def get_confirmation_menu():
    """Provides Yes/No options for confirmations."""
    keyboard = [
        [KeyboardButton(text="✅ Yes"), KeyboardButton(text="❌ No")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Please confirm your choice..."
    )

def get_navigation_menu():
    """Provides navigation options."""
    keyboard = [
        [KeyboardButton(text="⬅️ Previous"), KeyboardButton(text="➡️ Next")],
        [KeyboardButton(text="🔝 Top"), KeyboardButton(text="🔚 Bottom")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Navigate through options..."
    )
