import os
import httpx
import logging
from aiogram import Router, F, types, Bot
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BufferedInputFile,
)
from aiogram.fsm.context import FSMContext

from app.telegram.states.voice_note_states import VoiceNoteStates
from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action
from app.telegram.keyboards import inline_keyboards as ik
from app.utils.ids import extract_id

logger = logging.getLogger(__name__)
router = Router()

# Ensure the URL is clean without trailing slashes
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

# --- Helpers ---
def get_trade_label(t):
    """Safely extracts label info from a trade dictionary."""
    if not isinstance(t, dict):
        return f"Trade {t}"
    
    t_id = t.get("id", "??")
    symbol = t.get("symbol", "Unknown")
    created_at = t.get("created_at") or ""
    date_str = created_at.split("T")[0] if "T" in created_at else "No Date"
    return f"ID:{t_id} | {symbol} | {date_str}"

def ensure_list(data):
    """Ensures API response is a list, handling paginated wrappers."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ["trades", "items", "results", "notes"]:
            if key in data and isinstance(data[key], list):
                return data[key]
    return []

# --- Menu Handlers ---
@router.message(F.text == "🎙️ Voice Notes")
async def show_voice_note_menu(message: Message, state: FSMContext):
    await message.answer(
        "🎙️ <b>Voice Note Management</b>\nSelect an action below:",
        reply_markup=ik.get_voice_note_options(),
        parse_mode="HTML",
    )

# --- Record Logic ---
@router.callback_query(F.data == "voice_record")
async def list_trades_for_record(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth, acc_id = user_data.get("access_token"), user_data.get("active_account_id")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trades?account_id={acc_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )
        trades = ensure_list(resp.json())

        btns = [
            [
                InlineKeyboardButton(
                    text=f"🎤 {get_trade_label(t)}",
                    callback_data=f"vn_target_{t['id']}_{t.get('state', 'OPEN')}",
                )
            ]
            for t in trades if isinstance(t, dict)
        ]

        await callback.message.edit_text(
            "<b>Select trade to record for:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML",
        )
        await state.set_state(VoiceNoteStates.waiting_for_trade_selection)
    await callback.answer()

@router.callback_query(VoiceNoteStates.waiting_for_trade_selection, F.data.startswith("vn_target_"))
async def process_target_trade(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    # parts: [vn, target, trade_id, trade_state]
    await state.update_data(vn_trade_id=str(parts[2]), vn_trade_state=str(parts[3]))

    await callback.message.answer(
        "🎤 <b>Recording...</b>\nSend your voice message or audio file:",
        reply_markup=get_cancel_action(),
        parse_mode="HTML",
    )
    await state.set_state(VoiceNoteStates.waiting_for_voice)
    await callback.answer()

@router.message(VoiceNoteStates.waiting_for_voice, F.voice | F.audio)
async def handle_upload(message: Message, state: FSMContext, bot: Bot):
    """Downloads voice from Telegram and uploads to FastAPI using Form Data."""
    data = await state.get_data()
    auth = data.get("access_token")
    trade_id = data.get("vn_trade_id")
    trade_state = data.get("vn_trade_state")

    media = message.voice or message.audio
    file_info = await bot.get_file(media.file_id)
    file_content = await bot.download_file(file_info.file_path)

    async with httpx.AsyncClient() as client:
        # Your FastAPI uses @router.post("") on the "voice-notes" prefix
        url = f"{BOT_BACKEND_URL}/api/v1/voice-notes"
        
        # FastAPI Form(...) fields must be sent in 'data', not 'params'
        form_data = {
            "trade_id": str(trade_id),
            "trade_state_at_time": str(trade_state)
        }
        files = {'file': (f"note_{trade_id}.ogg", file_content, 'audio/ogg')}
        
        resp = await client.post(
            url, 
            headers={"Authorization": f"Bearer {auth}"},
            data=form_data, 
            files=files
        )

        if resp.status_code in [200, 201]:
            await message.answer(
                "✅ <b>Voice note saved successfully!</b>", 
                reply_markup=get_main_menu(), 
                parse_mode="HTML"
            )
            await state.clear()
        else:
            logger.error(f"Upload failed {resp.status_code}: {resp.text}")
            await message.answer(f"❌ Failed to save note. (Error {resp.status_code})")

# --- Listing / Playback Logic ---
@router.callback_query(F.data.in_(["voice_view_list", "voice_delete_list"]))
async def list_trades_for_notes(callback: types.CallbackQuery, state: FSMContext):
    action = "view" if "view" in callback.data else "delete"
    user_data = await state.get_data() or {}
    auth, acc_id = user_data.get("access_token"), user_data.get("active_account_id")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trades?account_id={acc_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )
        trades = ensure_list(resp.json())

        btns = [
            [
                InlineKeyboardButton(
                    text=f"📂 {get_trade_label(t)}",
                    callback_data=f"vn_{action}_list_{t['id']}",
                )
            ]
            for t in trades if isinstance(t, dict)
        ]

        await callback.message.edit_text(
            f"<b>Select trade to {action} notes:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML",
        )
    await callback.answer()

@router.callback_query(F.data.startswith("vn_view_list_"))
async def show_notes_to_play(callback: types.CallbackQuery, state: FSMContext):
    trade_id = extract_id(callback.data, "vn_view_list")
    auth = (await state.get_data() or {}).get("access_token")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/voice-notes/trade/{trade_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )
        notes = ensure_list(resp.json())

        if not notes:
            return await callback.message.answer("No notes found for this trade.")

        btns = [
            [
                InlineKeyboardButton(
                    text=f"🔊 Play Note #{n['id']} ({n.get('trade_state_at_time', 'N/A')})",
                    callback_data=f"play_vn_{n['id']}",
                )
            ]
            for n in notes if isinstance(n, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Back", callback_data="voice_view_list")])

        await callback.message.edit_text(
            "<b>Select a note to play:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML",
        )
    await callback.answer()

@router.callback_query(F.data.startswith("play_vn_"))
async def process_play_note(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    note_id = extract_id(callback.data, "play_vn")
    auth = (await state.get_data() or {}).get("access_token")

    async with httpx.AsyncClient() as client:
        meta_resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/voice-notes/{note_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )
        if meta_resp.status_code == 200:
            path = meta_resp.json().get("file_path").lstrip("/")
            file_resp = await client.get(
                f"{BOT_BACKEND_URL}/{path}",
                headers={"Authorization": f"Bearer {auth}"},
            )
            
            voice = BufferedInputFile(file_resp.content, filename=f"note_{note_id}.ogg")
            await callback.message.answer_voice(voice=voice, caption=f"🎵 Trade Note #{note_id}")
        else:
            await callback.answer("Note not found on server.", show_alert=True)
    await callback.answer()

# --- Delete Logic ---
@router.callback_query(F.data.startswith("vn_delete_list_"))
async def show_notes_to_delete(callback: types.CallbackQuery, state: FSMContext):
    trade_id = extract_id(callback.data, "vn_delete_list")
    auth = (await state.get_data() or {}).get("access_token")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/voice-notes/trade/{trade_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )
        notes = ensure_list(resp.json())

        if not notes:
            return await callback.message.answer("No notes found.")

        btns = [
            [
                InlineKeyboardButton(
                    text=f"🗑️ Delete Note #{n['id']}",
                    callback_data=f"drop_vn_{n['id']}",
                )
            ]
            for n in notes if isinstance(n, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Back", callback_data="voice_delete_list")])

        await callback.message.edit_text(
            "<b>⚠️ Select a note to PERMANENTLY delete:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML",
        )
    await callback.answer()

@router.callback_query(F.data.startswith("drop_vn_"))
async def process_note_deletion(callback: types.CallbackQuery, state: FSMContext):
    note_id = extract_id(callback.data, "drop_vn")
    auth = (await state.get_data() or {}).get("access_token")

    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{BOT_BACKEND_URL}/api/v1/voice-notes/{note_id}",
            headers={"Authorization": f"Bearer {auth}"},
        )

        if res.status_code == 204:
            await callback.message.answer("✅ <b>Voice note deleted.</b>", parse_mode="HTML")
            await callback.message.delete()
    await callback.answer()
