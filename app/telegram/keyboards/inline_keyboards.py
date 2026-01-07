from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_account_options():
    """Maps to /api/v1/accounts logic."""
    buttons = [
        [InlineKeyboardButton(text="➕ Create Account", callback_data="account_create")],
        [InlineKeyboardButton(text="🔄 Switch Active", callback_data="account_switch")],
        [InlineKeyboardButton(text="🗑️ Delete Account", callback_data="account_delete")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_trade_management():
    """Maps to /api/v1/trades logic."""
    buttons = [
        [InlineKeyboardButton(text="📈 Open Trade", callback_data="trade_open")],
        [InlineKeyboardButton(text="❌ Close Trade", callback_data="trade_close")],
        [InlineKeyboardButton(text="🔄 Modify Trade", callback_data="trade_modify")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_psychology_tools():
    """Maps to /api/v1/psychology logic."""
    buttons = [
        [InlineKeyboardButton(text="🧘 Start Session", callback_data="psych_start")],
        [InlineKeyboardButton(text="📊 View Stats", callback_data="psych_stats")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_media_options():
    """Maps to /api/v1/media logic."""
    buttons = [
        [InlineKeyboardButton(text="📤 Upload Media", callback_data="media_upload")],
        [InlineKeyboardButton(text="📥 Download Media", callback_data="media_download")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_activity_log():
    """Maps to /api/v1/activity logic."""
    buttons = [
        [InlineKeyboardButton(text="🕒 View Recent Activity", callback_data="activity_recent")],
        [InlineKeyboardButton(text="📅 View Activity by Date", callback_data="activity_date")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)    
