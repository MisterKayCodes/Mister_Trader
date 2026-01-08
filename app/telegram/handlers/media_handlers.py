import os
import httpx
import logging
from aiogram import Router, F, types, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext

from app.telegram.states.media_states import MediaStates
from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action
from app.telegram.keyboards import inline_keyboards as ik

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

def _check_session(user_data: dict) -> bool:
    return bool(user_data.get("access_token") and user_data.get("active_account_id"))

async def _fetch_trades(auth: str, acc_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trades?account_id={acc_id}",
            headers={"Authorization": f"Bearer {auth}"},
            timeout=10.0
        )
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("trades", data.get("items", []))

def _get_trade_label(t: dict) -> str:
    t_id = t.get("id", "??")
    symbol = t.get("symbol", "Unknown")
    state = t.get("state", "N/A")
    return f"ID:{t_id} | {symbol} | {state}"

@router.message(F.text == "🖼️ Trade Media")
async def show_media_menu(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    active_vault = user_data.get("active_account_name", "N/A")
    
    await message.answer(
        f"🖼️ <b>Trade Media Management</b>\n"
        f"Active Vault: <code>{active_vault}</code>\n\n"
        f"Upload screenshots or view trade images.",
        reply_markup=ik.get_media_options(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "media_upload")
async def start_media_upload(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing or no active vault.", show_alert=True)
    
    try:
        trades = await _fetch_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found. Log a trade first before uploading media.")
        
        btns = [
            [InlineKeyboardButton(
                text=f"📤 {_get_trade_label(t)}",
                callback_data=f"media_target_{t['id']}"
            )]
            for t in trades if isinstance(t, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Cancel", callback_data="menu_main")])
        
        await callback.message.edit_text(
            "<b>Select a trade to upload media for:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML"
        )
        await state.set_state(MediaStates.waiting_for_trade_selection)
    except Exception as e:
        logger.error(f"Fetch trades error: {e}")
        await callback.answer("❌ Failed to load trades.", show_alert=True)
    await callback.answer()

@router.callback_query(MediaStates.waiting_for_trade_selection, F.data.startswith("media_target_"))
async def process_media_trade_selection(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    await state.update_data(media_trade_id=trade_id)
    
    btns = [
        [InlineKeyboardButton(text="📸 Screenshot", callback_data="mtype_screenshot")],
        [InlineKeyboardButton(text="📊 Chart", callback_data="mtype_chart")],
        [InlineKeyboardButton(text="📈 Entry Setup", callback_data="mtype_entry")],
        [InlineKeyboardButton(text="📉 Exit Result", callback_data="mtype_exit")],
        [InlineKeyboardButton(text="🔙 Cancel", callback_data="menu_main")],
    ]
    
    await callback.message.edit_text(
        f"<b>Trade ID {trade_id}</b>\n\n"
        f"📁 <b>Select media type:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(MediaStates.waiting_for_media_type)
    await callback.answer()

@router.callback_query(MediaStates.waiting_for_media_type, F.data.startswith("mtype_"))
async def process_media_type(callback: CallbackQuery, state: FSMContext):
    media_type = callback.data.replace("mtype_", "")
    await state.update_data(media_type=media_type)
    
    data = await state.get_data()
    await callback.message.answer(
        f"<b>Trade ID {data['media_trade_id']}</b>\n"
        f"<b>Type:</b> {media_type}\n\n"
        f"📤 <b>Send your image now:</b>",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(MediaStates.waiting_for_file)
    await callback.answer()

@router.message(MediaStates.waiting_for_file, F.photo)
async def handle_media_upload(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data() or {}
    auth = data.get("access_token")
    trade_id = data.get("media_trade_id")
    media_type = data.get("media_type", "screenshot")
    
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_content = await bot.download_file(file_info.file_path)
    
    async with httpx.AsyncClient() as client:
        form_data = {
            "trade_id": str(trade_id),
            "media_type": media_type
        }
        files = {'file': (f"trade_{trade_id}_{media_type}.jpg", file_content, 'image/jpeg')}
        
        try:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/trade-media/",
                headers={"Authorization": f"Bearer {auth}"},
                data=form_data,
                files=files,
                timeout=30.0
            )
            
            if resp.status_code in [200, 201]:
                await state.set_state(None)
                await message.answer(
                    f"✅ <b>Media uploaded successfully!</b>\n\n"
                    f"📁 Trade: {trade_id}\n"
                    f"📸 Type: {media_type}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = resp.json().get("detail", "Unknown error")
                logger.error(f"Upload failed: {resp.status_code} - {detail}")
                await message.answer(f"❌ <b>Upload failed:</b> {detail}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Media upload error: {e}")
            await message.answer("❌ Connection failure during upload.")

@router.message(MediaStates.waiting_for_file, F.document)
async def handle_document_upload(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data() or {}
    auth = data.get("access_token")
    trade_id = data.get("media_trade_id")
    media_type = data.get("media_type", "document")
    
    doc = message.document
    if not doc.mime_type or not doc.mime_type.startswith("image/"):
        return await message.answer("❌ Please send an image file only.")
    
    file_info = await bot.get_file(doc.file_id)
    file_content = await bot.download_file(file_info.file_path)
    
    async with httpx.AsyncClient() as client:
        form_data = {
            "trade_id": str(trade_id),
            "media_type": media_type
        }
        ext = doc.file_name.split(".")[-1] if doc.file_name else "jpg"
        files = {'file': (f"trade_{trade_id}_{media_type}.{ext}", file_content, doc.mime_type)}
        
        try:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/trade-media/",
                headers={"Authorization": f"Bearer {auth}"},
                data=form_data,
                files=files,
                timeout=30.0
            )
            
            if resp.status_code in [200, 201]:
                await state.set_state(None)
                await message.answer(
                    f"✅ <b>Media uploaded successfully!</b>",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                await message.answer("❌ Upload failed.")
        except Exception as e:
            logger.error(f"Doc upload error: {e}")
            await message.answer("❌ Connection failure.")

@router.callback_query(F.data == "media_download")
async def list_trades_for_media_view(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    try:
        trades = await _fetch_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found.")
        
        btns = [
            [InlineKeyboardButton(
                text=f"📂 {_get_trade_label(t)}",
                callback_data=f"view_media_{t['id']}"
            )]
            for t in trades if isinstance(t, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")])
        
        await callback.message.edit_text(
            "<b>Select a trade to view media:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"View media trades error: {e}")
        await callback.answer("❌ Error.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data.startswith("view_media_"))
async def show_trade_media(callback: CallbackQuery, state: FSMContext, bot: Bot):
    trade_id = callback.data.split("_")[2]
    auth = (await state.get_data() or {}).get("access_token")
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/trade-media/trade/{trade_id}",
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code == 200:
                media_list = resp.json()
                if not media_list:
                    return await callback.message.answer(f"No media found for Trade {trade_id}.")
                
                await callback.message.answer(f"📂 <b>Media for Trade {trade_id}</b> ({len(media_list)} files):", parse_mode="HTML")
                
                for item in media_list[:5]:
                    path = item.get("file_path", "").lstrip("/")
                    media_type = item.get("media_type", "image")
                    
                    try:
                        file_resp = await client.get(
                            f"{BOT_BACKEND_URL}/{path}",
                            headers={"Authorization": f"Bearer {auth}"},
                            timeout=15.0
                        )
                        if file_resp.status_code == 200:
                            photo = BufferedInputFile(file_resp.content, filename=os.path.basename(path))
                            await callback.message.answer_photo(
                                photo,
                                caption=f"📸 {media_type.title()} | Media #{item['id']}"
                            )
                    except Exception as e:
                        logger.error(f"File download error: {e}")
                        await callback.message.answer(f"❌ Failed to load media #{item['id']}")
            else:
                await callback.message.answer(f"No media found for Trade {trade_id}.")
        except Exception as e:
            logger.error(f"View media error: {e}")
            await callback.answer("❌ Connection error.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data == "media_view")
async def legacy_media_view(callback: CallbackQuery, state: FSMContext):
    await list_trades_for_media_view(callback, state)
