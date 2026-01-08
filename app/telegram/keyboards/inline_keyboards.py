from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_account_options():
    buttons = [
        [InlineKeyboardButton(text="➕ Create Account", callback_data="account_create")],
        [InlineKeyboardButton(text="🔄 Switch Active", callback_data="account_switch")],
        [InlineKeyboardButton(text="🗑️ Delete Account", callback_data="account_delete")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_trade_management():
    buttons = [
        [InlineKeyboardButton(text="📈 Open Trade", callback_data="trade_open")],
        [InlineKeyboardButton(text="❌ Close Trade", callback_data="trade_close")],
        [InlineKeyboardButton(text="👁️ View Trades", callback_data="trade_view")],
        [InlineKeyboardButton(text="🔄 Modify Trade", callback_data="trade_modify")],
        [InlineKeyboardButton(text="🗑️ Delete Trade", callback_data="trade_delete")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_trade_side_options():
    buttons = [
        [
            InlineKeyboardButton(text="BUY 🟢", callback_data="side_BUY"),
            InlineKeyboardButton(text="SELL 🔴", callback_data="side_SELL")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_modify_field_options():
    buttons = [
        [InlineKeyboardButton(text="🔢 Change Lot Size", callback_data="mod_field_quantity")],
        [InlineKeyboardButton(text="💰 Change Entry Price", callback_data="mod_field_entry_price")],
        [InlineKeyboardButton(text="🔙 Cancel", callback_data="trade_view")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_voice_note_options():
    buttons = [
        [InlineKeyboardButton(text="🎙️ Record/Upload Note", callback_data="voice_record")],
        [InlineKeyboardButton(text="🎧 Listen to Notes", callback_data="voice_view_list")],
        [InlineKeyboardButton(text="🗑️ Delete a Note", callback_data="voice_delete_list")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_psychology_tools():
    buttons = [
        [InlineKeyboardButton(text="🧘 Start Session", callback_data="psych_start")],
        [InlineKeyboardButton(text="👁️ View Entries", callback_data="psych_view")],
        [InlineKeyboardButton(text="📊 View Stats", callback_data="psych_stats")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_media_options():
    buttons = [
        [InlineKeyboardButton(text="📤 Upload Media", callback_data="media_upload")],
        [InlineKeyboardButton(text="📥 View Media", callback_data="media_download")],
        [InlineKeyboardButton(text="🗑️ Delete Media", callback_data="media_delete")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_activity_log():
    buttons = [
        [InlineKeyboardButton(text="📝 Log Activity", callback_data="activity_log")],
        [InlineKeyboardButton(text="🕒 View Recent", callback_data="activity_recent")],
        [InlineKeyboardButton(text="📅 View by Date", callback_data="activity_date")],
        [InlineKeyboardButton(text="🗑️ Delete Activity", callback_data="activity_delete")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_stats_navigation():
    """Inline keyboard for navigating between stats views."""
    buttons = [
        [
            InlineKeyboardButton(text="📊 Overview", callback_data="stats:overview"),
            InlineKeyboardButton(text="🌍 Sessions", callback_data="stats:sessions")
        ],
        [
            InlineKeyboardButton(text="📋 Strategies", callback_data="stats:strategies"),
            InlineKeyboardButton(text="🔥 Streaks", callback_data="stats:streak")
        ],
        [
            InlineKeyboardButton(text="⏰ Time Analysis", callback_data="stats:time"),
            InlineKeyboardButton(text="🔄 Refresh", callback_data="stats:refresh")
        ],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_strategy_options():
    """Inline keyboard for strategy management."""
    buttons = [
        [InlineKeyboardButton(text="➕ Create Strategy", callback_data="strategy:new")],
        [InlineKeyboardButton(text="👁️ View Strategies", callback_data="strategy:list")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_plan_options():
    """Inline keyboard for trading plan management."""
    buttons = [
        [InlineKeyboardButton(text="➕ Create Plan", callback_data="plan:new")],
        [InlineKeyboardButton(text="📅 Today's Plan", callback_data="plan:today")],
        [InlineKeyboardButton(text="📋 View All Plans", callback_data="plan:list")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_export_options():
    """Inline keyboard for export options."""
    buttons = [
        [InlineKeyboardButton(text="📊 Export All Trades", callback_data="export:all")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
