import os
import httpx
import logging
from datetime import date, datetime
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.telegram.states.activity_states import ActivityStates
from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action
from app.telegram.keyboards import inline_keyboards as ik

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

def _check_session(user_data: dict) -> bool:
    return bool(user_data.get("access_token"))

ACTIVITY_TYPES = [
    ("📊", "trade_opened", "Trade Opened"),
    ("✅", "trade_closed", "Trade Closed"),
    ("📈", "analysis", "Market Analysis"),
    ("📚", "study", "Study Session"),
    ("🧘", "mindfulness", "Mindfulness"),
    ("📝", "journal", "Journal Entry"),
]

@router.message(F.text == "📈 Activity")
async def show_activity_menu(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    
    await message.answer(
        "📈 <b>Activity Log</b>\n\n"
        "Track your daily trading activities and habits.",
        reply_markup=ik.get_activity_log(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "activity_log")
async def start_activity_log(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    btns = [
        [InlineKeyboardButton(text=f"{emoji} {label}", callback_data=f"atype_{code}")]
        for emoji, code, label in ACTIVITY_TYPES
    ]
    btns.append([InlineKeyboardButton(text="🔙 Cancel", callback_data="menu_main")])
    
    await callback.message.edit_text(
        "<b>Log New Activity</b>\n\n"
        "Select an activity type:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(ActivityStates.waiting_for_activity_type)
    await callback.answer()

@router.callback_query(ActivityStates.waiting_for_activity_type, F.data.startswith("atype_"))
async def process_activity_type(callback: CallbackQuery, state: FSMContext):
    activity_type = callback.data.replace("atype_", "")
    await state.update_data(activity_type=activity_type)
    
    today = date.today().isoformat()
    btns = [
        [InlineKeyboardButton(text=f"📅 Today ({today})", callback_data="adate_today")],
        [InlineKeyboardButton(text="📆 Enter Custom Date", callback_data="adate_custom")],
        [InlineKeyboardButton(text="🔙 Cancel", callback_data="menu_main")],
    ]
    
    label = next((l for e, c, l in ACTIVITY_TYPES if c == activity_type), activity_type)
    await callback.message.edit_text(
        f"<b>Activity:</b> {label} ✅\n\n"
        "📅 <b>Select date:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(ActivityStates.waiting_for_date)
    await callback.answer()

@router.callback_query(ActivityStates.waiting_for_date, F.data == "adate_today")
async def process_today_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data() or {}
    auth = data.get("access_token")
    activity_type = data.get("activity_type")
    today = date.today().isoformat()
    
    await _submit_activity(callback.message, state, auth, activity_type, today)
    await callback.answer()

@router.callback_query(ActivityStates.waiting_for_date, F.data == "adate_custom")
async def prompt_custom_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📆 <b>Enter date (YYYY-MM-DD):</b>\n"
        "Example: <code>2026-01-08</code>",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(ActivityStates.waiting_for_date)
async def process_custom_date(message: Message, state: FSMContext):
    text = message.text.strip()
    
    try:
        parsed_date = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return await message.answer(
            "❌ Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-08)",
            parse_mode="HTML"
        )
    
    data = await state.get_data() or {}
    auth = data.get("access_token")
    activity_type = data.get("activity_type")
    
    await _submit_activity(message, state, auth, activity_type, parsed_date.isoformat())

async def _submit_activity(message: Message, state: FSMContext, auth: str, activity_type: str, activity_date: str):
    payload = {
        "activity_type": activity_type,
        "date": activity_date
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/activities",
                json=payload,
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code in [200, 201]:
                await state.set_state(None)
                label = next((l for e, c, l in ACTIVITY_TYPES if c == activity_type), activity_type)
                await message.answer(
                    f"✅ <b>Activity logged!</b>\n\n"
                    f"📊 Type: {label}\n"
                    f"📅 Date: {activity_date}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = resp.json().get("detail", "Unknown error")
                await message.answer(f"❌ <b>Error:</b> {detail}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Activity submit error: {e}")
            await message.answer("❌ Connection failure.")

@router.callback_query(F.data == "activity_recent")
async def show_recent_activity(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    auth = user_data["access_token"]
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/activities",
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code == 200:
                activities = resp.json()
                if not activities:
                    return await callback.message.answer(
                        "📈 <b>Recent Activity</b>\n\n"
                        "No activities logged yet.\n"
                        "Use 'Log Activity' to start tracking.",
                        parse_mode="HTML"
                    )
                
                msg = "📈 <b>Recent Activity</b>\n\n"
                for act in activities[:10]:
                    act_type = act.get("activity_type", "Unknown")
                    act_date = act.get("date", "").split("T")[0]
                    emoji = next((e for e, c, l in ACTIVITY_TYPES if c == act_type), "📌")
                    label = next((l for e, c, l in ACTIVITY_TYPES if c == act_type), act_type)
                    msg += f"{emoji} {label} - <code>{act_date}</code>\n"
                
                await callback.message.answer(msg, parse_mode="HTML")
            else:
                await callback.answer("❌ Failed to fetch activities.", show_alert=True)
        except Exception as e:
            logger.error(f"Activity view error: {e}")
            await callback.answer("❌ Connection error.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data == "activity_date")
async def prompt_date_filter(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    await callback.message.answer(
        "📅 <b>Filter by Date</b>\n\n"
        "Enter date (YYYY-MM-DD):",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(ActivityStates.waiting_for_date)
    await state.update_data(activity_filter_mode=True)
    await callback.answer()

@router.callback_query(F.data == "activity_view")
async def legacy_activity_view(callback: CallbackQuery, state: FSMContext):
    await show_recent_activity(callback, state)

@router.callback_query(F.data == "activity_delete")
async def list_activities_for_deletion(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    auth = user_data["access_token"]
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/activities",
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code == 200:
                activities = resp.json()
                if not activities:
                    return await callback.message.answer("No activities to delete.")
                
                btns = []
                for act in activities[:10]:
                    act_type = act.get("activity_type", "Unknown")
                    act_date = act.get("date", "").split("T")[0]
                    label = next((l for e, c, l in ACTIVITY_TYPES if c == act_type), act_type)
                    btns.append([InlineKeyboardButton(
                        text=f"🗑️ {label} ({act_date})",
                        callback_data=f"del_act_{act['id']}"
                    )])
                btns.append([InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")])
                
                await callback.message.edit_text(
                    "<b>⚠️ Select activity to delete:</b>",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
                    parse_mode="HTML"
                )
            else:
                await callback.answer("❌ Failed to fetch activities.", show_alert=True)
        except Exception as e:
            logger.error(f"Delete list error: {e}")
            await callback.answer("❌ Error.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data.startswith("del_act_"))
async def process_activity_deletion(callback: CallbackQuery, state: FSMContext):
    activity_id = callback.data.split("_")[2]
    auth = (await state.get_data() or {}).get("access_token")
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.delete(
                f"{BOT_BACKEND_URL}/api/v1/activities/{activity_id}",
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code == 204:
                await callback.message.answer(
                    "✅ <b>Activity deleted.</b>",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                await callback.answer("❌ Failed to delete.", show_alert=True)
        except Exception as e:
            logger.error(f"Delete activity error: {e}")
            await callback.answer("❌ Error.", show_alert=True)
    await callback.answer()
