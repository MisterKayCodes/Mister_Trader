import os
import httpx
import logging
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.telegram.states.psychology_states import PsychologyStates
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

@router.message(F.text == "🧠 Psychology")
async def show_psychology_menu(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    active_vault = user_data.get("active_account_name", "N/A")
    
    await message.answer(
        f"🧠 <b>Psychology & Discipline</b>\n"
        f"Active Vault: <code>{active_vault}</code>\n\n"
        f"Log your emotional state and trading discipline.",
        reply_markup=ik.get_psychology_tools(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "psych_start")
async def start_psychology_session(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing or no active vault.", show_alert=True)
    
    auth = user_data["access_token"]
    acc_id = user_data["active_account_id"]
    
    try:
        trades = await _fetch_trades(auth, acc_id)
        if not trades:
            return await callback.message.answer("No trades found. Log a trade first before adding psychology notes.")
        
        btns = [
            [InlineKeyboardButton(
                text=f"🧠 {_get_trade_label(t)}",
                callback_data=f"psych_trade_{t['id']}"
            )]
            for t in trades if isinstance(t, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Cancel", callback_data="menu_main")])
        
        await callback.message.edit_text(
            "<b>Select a trade to log psychology for:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML"
        )
        await state.set_state(PsychologyStates.waiting_for_trade_selection)
    except Exception as e:
        logger.error(f"Fetch trades error: {e}")
        await callback.answer("❌ Failed to load trades.", show_alert=True)
    await callback.answer()

@router.callback_query(PsychologyStates.waiting_for_trade_selection, F.data.startswith("psych_trade_"))
async def process_trade_selection(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    user_data = await state.get_data() or {}
    await state.update_data(
        psych_trade_id=trade_id,
        psych_auth=user_data.get("access_token")
    )
    
    btns = [
        [
            InlineKeyboardButton(text="1️⃣", callback_data="disc_1"),
            InlineKeyboardButton(text="2️⃣", callback_data="disc_2"),
            InlineKeyboardButton(text="3️⃣", callback_data="disc_3"),
            InlineKeyboardButton(text="4️⃣", callback_data="disc_4"),
            InlineKeyboardButton(text="5️⃣", callback_data="disc_5"),
        ]
    ]
    
    await callback.message.edit_text(
        f"<b>Trade ID {trade_id}</b>\n\n"
        f"📊 <b>Rate your discipline (1-5):</b>\n"
        f"1 = Poor, 5 = Excellent",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(PsychologyStates.waiting_for_discipline)
    await callback.answer()

@router.callback_query(PsychologyStates.waiting_for_discipline, F.data.startswith("disc_"))
async def process_discipline(callback: CallbackQuery, state: FSMContext):
    discipline = int(callback.data.split("_")[1])
    await state.update_data(psych_discipline=discipline)
    
    btns = [
        [
            InlineKeyboardButton(text="1️⃣", callback_data="conf_1"),
            InlineKeyboardButton(text="2️⃣", callback_data="conf_2"),
            InlineKeyboardButton(text="3️⃣", callback_data="conf_3"),
            InlineKeyboardButton(text="4️⃣", callback_data="conf_4"),
            InlineKeyboardButton(text="5️⃣", callback_data="conf_5"),
        ]
    ]
    
    await callback.message.edit_text(
        f"<b>Discipline:</b> {discipline}/5 ✅\n\n"
        f"💪 <b>Rate your confidence (1-5):</b>\n"
        f"1 = Very Low, 5 = Very High",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(PsychologyStates.waiting_for_confidence)
    await callback.answer()

@router.callback_query(PsychologyStates.waiting_for_confidence, F.data.startswith("conf_"))
async def process_confidence(callback: CallbackQuery, state: FSMContext):
    confidence = int(callback.data.split("_")[1])
    await state.update_data(psych_confidence=confidence)
    
    btns = [
        [
            InlineKeyboardButton(text="✅ Yes", callback_data="plan_true"),
            InlineKeyboardButton(text="❌ No", callback_data="plan_false"),
        ]
    ]
    
    data = await state.get_data()
    await callback.message.edit_text(
        f"<b>Discipline:</b> {data['psych_discipline']}/5 ✅\n"
        f"<b>Confidence:</b> {confidence}/5 ✅\n\n"
        f"📋 <b>Did you follow your trading plan?</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
        parse_mode="HTML"
    )
    await state.set_state(PsychologyStates.waiting_for_plan_check)
    await callback.answer()

@router.callback_query(PsychologyStates.waiting_for_plan_check, F.data.startswith("plan_"))
async def process_plan_check(callback: CallbackQuery, state: FSMContext):
    followed_plan = callback.data.split("_")[1] == "true"
    await state.update_data(psych_followed_plan=followed_plan)
    
    await callback.message.answer(
        "📝 <b>Any notes for this trade?</b>\n"
        "Type your notes or send <code>skip</code> to finish.",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(PsychologyStates.waiting_for_notes)
    await callback.answer()

@router.message(PsychologyStates.waiting_for_notes)
async def process_notes_and_submit(message: Message, state: FSMContext):
    notes = message.text.strip() if message.text.lower() != "skip" else ""
    data = await state.get_data() or {}
    auth = data.get("psych_auth") or data.get("access_token")
    
    if not auth:
        return await message.answer("❌ Session expired. Please /login again.")
    
    payload = {
        "trade_id": int(data["psych_trade_id"]),
        "discipline": data["psych_discipline"],
        "confidence": data["psych_confidence"],
        "followed_plan": data["psych_followed_plan"],
        "notes": notes
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/trade-psychology/",
                json=payload,
                headers={"Authorization": f"Bearer {auth}"},
                timeout=10.0
            )
            
            if resp.status_code in [200, 201]:
                await state.set_state(None)
                await message.answer(
                    f"✅ <b>Psychology logged!</b>\n\n"
                    f"📊 Discipline: {data['psych_discipline']}/5\n"
                    f"💪 Confidence: {data['psych_confidence']}/5\n"
                    f"📋 Followed Plan: {'Yes ✅' if data['psych_followed_plan'] else 'No ❌'}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = resp.json().get("detail", "Unknown error")
                await message.answer(f"❌ <b>Error:</b> {detail}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Psychology submit error: {e}")
            await message.answer("❌ Connection failure.")

@router.callback_query(F.data == "psych_stats")
async def show_psychology_stats(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing or no active vault.", show_alert=True)
    
    auth = user_data["access_token"]
    acc_id = user_data["active_account_id"]
    
    try:
        trades = await _fetch_trades(auth, acc_id)
        if not trades:
            return await callback.message.answer(
                "📊 <b>Psychology Stats</b>\n\n"
                "No trades found. Log trades first to see stats.",
                parse_mode="HTML"
            )
        
        total_entries = 0
        total_discipline = 0
        total_confidence = 0
        followed_count = 0
        
        async with httpx.AsyncClient() as client:
            for t in trades:
                try:
                    resp = await client.get(
                        f"{BOT_BACKEND_URL}/api/v1/trade-psychology/trade/{t['id']}",
                        headers={"Authorization": f"Bearer {auth}"},
                        timeout=5.0
                    )
                    if resp.status_code == 200:
                        psych = resp.json()
                        total_entries += 1
                        total_discipline += psych.get("discipline", 0)
                        total_confidence += psych.get("confidence", 0)
                        if psych.get("followed_plan"):
                            followed_count += 1
                except:
                    continue
        
        if total_entries > 0:
            avg_discipline = total_discipline / total_entries
            avg_confidence = total_confidence / total_entries
            plan_adherence = (followed_count / total_entries) * 100
            
            msg = (
                "📊 <b>Psychology Stats</b>\n\n"
                f"📈 Trades Analyzed: <code>{total_entries}</code>\n"
                f"📊 Avg Discipline: <code>{avg_discipline:.1f}/5</code>\n"
                f"💪 Avg Confidence: <code>{avg_confidence:.1f}/5</code>\n"
                f"📋 Plan Adherence: <code>{plan_adherence:.0f}%</code>"
            )
        else:
            msg = (
                "📊 <b>Psychology Stats</b>\n\n"
                "No psychology entries found.\n"
                "Use 'Start Session' to log your first entry."
            )
        
        await callback.message.answer(msg, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Psychology stats error: {e}")
        await callback.answer("❌ Error loading stats.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data == "psych_view")
async def view_psychology_entries(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_session(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    try:
        trades = await _fetch_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found.")
        
        btns = [
            [InlineKeyboardButton(
                text=f"👁️ {_get_trade_label(t)}",
                callback_data=f"view_psych_{t['id']}"
            )]
            for t in trades if isinstance(t, dict)
        ]
        btns.append([InlineKeyboardButton(text="🔙 Back", callback_data="menu_main")])
        
        await callback.message.edit_text(
            "<b>Select a trade to view psychology:</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"View psych error: {e}")
        await callback.answer("❌ Error.", show_alert=True)
    await callback.answer()

@router.callback_query(F.data.startswith("view_psych_"))
async def show_trade_psychology(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    user_data = await state.get_data() or {}
    auth = user_data.get("access_token")
    
    if not auth:
        return await callback.answer("❌ Session expired.", show_alert=True)
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trade-psychology/trade/{trade_id}",
            headers={"Authorization": f"Bearer {auth}"},
            timeout=10.0
        )
        
        if resp.status_code == 200:
            p = resp.json()
            msg = (
                f"🧠 <b>Psychology for Trade {trade_id}</b>\n\n"
                f"📊 Discipline: <code>{p.get('discipline', 'N/A')}/5</code>\n"
                f"💪 Confidence: <code>{p.get('confidence', 'N/A')}/5</code>\n"
                f"📋 Followed Plan: {'✅ Yes' if p.get('followed_plan') else '❌ No'}\n"
                f"📝 Notes: <code>{p.get('notes', 'None')}</code>"
            )
            await callback.message.answer(msg, parse_mode="HTML")
        else:
            await callback.message.answer(f"No psychology entry found for Trade {trade_id}.")
    await callback.answer()
