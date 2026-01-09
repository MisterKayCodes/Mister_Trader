import os
import httpx
import logging
from datetime import datetime, timezone
from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action
from app.telegram.keyboards import inline_keyboards as ik
from app.utils.session_utils import detect_trading_session, get_session_display_name

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")


class TradeStates(StatesGroup):
    waiting_for_symbol = State()
    waiting_for_side = State()
    waiting_for_quantity = State()
    waiting_for_entry_price = State()
    waiting_for_strategy = State()
    waiting_for_plan = State()
    waiting_for_emotion = State()
    waiting_for_rr = State()
    waiting_for_custom_rr = State()
    
    waiting_for_trade_selection = State()
    waiting_for_exit_price = State()
    waiting_for_post_emotion = State()
    waiting_for_field_selection = State()
    waiting_for_new_value = State()


EMOTIONS = ["Confident", "Focused", "Patient", "Anxious", "FOMO", "Revenge", "Tired", "Neutral"]
RR_OPTIONS = ["1:1", "1:2", "1:3", "1:4", "1:5", "Custom", "Skip"]


def get_emotion_keyboard():
    builder = InlineKeyboardBuilder()
    for emotion in EMOTIONS:
        builder.button(text=emotion, callback_data=f"emotion:{emotion}")
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup()


def get_rr_keyboard():
    builder = InlineKeyboardBuilder()
    for rr in RR_OPTIONS:
        builder.button(text=rr, callback_data=f"rr:{rr}")
    builder.adjust(3, 3, 1)
    return builder.as_markup()


async def _fetch_user_trades(auth_token: str, account_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trades?account_id={account_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        response.raise_for_status()
        return response.json()


async def _fetch_strategies(auth_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/strategies/",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0
        )
        if response.status_code == 200:
            return response.json()
        return []


async def _fetch_todays_plan(auth_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/plans/today",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0
        )
        if response.status_code == 200:
            return response.json()
        return None


def _check_active_account(user_data):
    if not user_data.get("access_token") or not user_data.get("active_account_id"):
        return False
    return True


@router.message(F.text == "📊 Active Trades")
async def show_trade_menu(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    active_account = user_data.get("active_account_name", "N/A")

    await message.answer(
        f"📊 <b>Trade Management</b>\nActive Vault: <code>{active_account}</code>\n\nMonitor positions or log new entries.",
        reply_markup=ik.get_trade_management(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "trade_view")
async def handle_view_trades(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("Please set an Active Vault first.", show_alert=True)
    
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found in this vault.")
        
        msg = f"📝 <b>Trades in Vault: {user_data.get('active_account_name')}</b>\n"
        for t in trades:
            session_name = get_session_display_name(t.get('trading_session', '')) if t.get('trading_session') else ''
            session_str = f" [{session_name}]" if session_name else ""
            msg += f"• <code>ID {t['id']}</code>: {t['symbol']} {t['side']} @ {t['entry_price']} ({t['state']}){session_str}\n"
        
        await callback.message.answer(msg, parse_mode="HTML")
    except Exception as e:
        logger.error(f"View trades error: {e}")
        await callback.answer("Failed to fetch trades.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "trade_open")
async def start_open_trade(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("Please set an Active Vault first.", show_alert=True)

    now_utc = datetime.now(timezone.utc)
    session = detect_trading_session(now_utc)
    session_display = get_session_display_name(session)
    
    await state.update_data(
        trade_session=session,
        trade_open_time=now_utc.isoformat()
    )
    
    await callback.message.answer(
        f"📈 <b>Logging New Trade</b>\n"
        f"Session: <b>{session_display}</b> (auto-detected)\n\n"
        f"Enter asset symbol (e.g. XAUUSD, EURUSD):",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_symbol)
    await callback.answer()


@router.message(TradeStates.waiting_for_symbol)
async def process_symbol(message: Message, state: FSMContext):
    symbol = message.text.strip().upper()
    await state.update_data(symbol=symbol)
    await message.answer(
        f"Symbol: <code>{symbol}</code>\nSelect side:",
        reply_markup=ik.get_trade_side_options(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_side)


@router.callback_query(TradeStates.waiting_for_side, F.data.startswith("side_"))
async def process_side(callback: CallbackQuery, state: FSMContext):
    side_val = callback.data.split("_")[1]
    await state.update_data(side=side_val)
    
    await callback.message.answer(
        f"Side: <b>{side_val}</b>\nEnter lot size:",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_quantity)
    await callback.answer()


@router.message(TradeStates.waiting_for_quantity)
async def process_quantity(message: Message, state: FSMContext):
    try:
        qty = float(message.text.strip())
        await state.update_data(quantity=qty)
        await message.answer(
            f"Lot Size: <b>{qty}</b>\nEnter entry price:",
            parse_mode="HTML"
        )
        await state.set_state(TradeStates.waiting_for_entry_price)
    except ValueError:
        await message.answer("Enter a valid number for lot size:")


@router.message(TradeStates.waiting_for_entry_price)
async def process_entry_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip())
        await state.update_data(entry_price=price)
        
        user_data = await state.get_data()
        auth_token = user_data.get("access_token")
        
        strategies = await _fetch_strategies(auth_token)
        
        if strategies:
            builder = InlineKeyboardBuilder()
            for s in strategies[:8]:
                builder.button(text=s['name'], callback_data=f"strat:{s['id']}")
            builder.button(text="Skip", callback_data="strat:skip")
            builder.adjust(2)
            
            await message.answer(
                f"Entry: <b>${price}</b>\n\nSelect strategy used:",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
            await state.set_state(TradeStates.waiting_for_strategy)
        else:
            await state.update_data(strategy_id=None)
            await _check_for_plan(message, state)
    except ValueError:
        await message.answer("Enter a valid number for entry price:")


@router.callback_query(TradeStates.waiting_for_strategy, F.data.startswith("strat:"))
async def process_strategy(callback: CallbackQuery, state: FSMContext):
    strat_val = callback.data.split(":")[1]
    if strat_val != "skip":
        await state.update_data(strategy_id=int(strat_val))
    else:
        await state.update_data(strategy_id=None)
    
    await callback.answer()
    await _check_for_plan(callback.message, state)


async def _check_for_plan(message: Message, state: FSMContext):
    user_data = await state.get_data()
    auth_token = user_data.get("access_token")
    
    plan = await _fetch_todays_plan(auth_token)
    
    if plan:
        builder = InlineKeyboardBuilder()
        builder.button(text=f"Link: {plan['title']}", callback_data=f"plan:{plan['id']}")
        builder.button(text="Skip", callback_data="plan:skip")
        builder.adjust(1)
        
        await message.answer(
            f"Today's plan: <b>{plan['title']}</b>\n\nLink this trade to your plan?",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        await state.set_state(TradeStates.waiting_for_plan)
    else:
        await state.update_data(plan_id=None)
        await _ask_pre_emotion(message, state)


@router.callback_query(TradeStates.waiting_for_plan, F.data.startswith("plan:"))
async def process_plan(callback: CallbackQuery, state: FSMContext):
    plan_val = callback.data.split(":")[1]
    if plan_val != "skip":
        await state.update_data(plan_id=int(plan_val))
    else:
        await state.update_data(plan_id=None)
    
    await callback.answer()
    await _ask_pre_emotion(callback.message, state)


async def _ask_pre_emotion(message: Message, state: FSMContext):
    await message.answer(
        "How are you feeling about this trade?",
        reply_markup=get_emotion_keyboard()
    )
    await state.set_state(TradeStates.waiting_for_emotion)


@router.callback_query(TradeStates.waiting_for_emotion, F.data.startswith("emotion:"))
async def process_pre_emotion(callback: CallbackQuery, state: FSMContext):
    emotion = callback.data.split(":")[1]
    await state.update_data(pre_trade_emotion=emotion)
    
    await callback.message.answer(
        f"Emotion: <b>{emotion}</b>\n\nSelect your planned Risk:Reward ratio:",
        reply_markup=get_rr_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_rr)
    await callback.answer()


@router.callback_query(TradeStates.waiting_for_rr, F.data.startswith("rr:"))
async def process_rr(callback: CallbackQuery, state: FSMContext):
    rr_val = callback.data.split(":")[1]
    
    if rr_val == "Custom":
        await callback.message.answer("Enter your custom R:R (e.g. 2.5):")
        await state.set_state(TradeStates.waiting_for_custom_rr)
        await callback.answer()
        return
    
    if rr_val == "Skip":
        await state.update_data(risk_reward_ratio=None)
    else:
        rr_float = float(rr_val.split(":")[1])
        await state.update_data(risk_reward_ratio=rr_float)
    
    await callback.answer()
    await _create_trade(callback.message, state)


@router.message(TradeStates.waiting_for_custom_rr)
async def process_custom_rr(message: Message, state: FSMContext):
    try:
        rr = float(message.text.strip())
        await state.update_data(risk_reward_ratio=rr)
        await _create_trade(message, state)
    except ValueError:
        await message.answer("Enter a valid number (e.g. 2.5):")


async def _create_trade(message: Message, state: FSMContext):
    data = await state.get_data()
    
    payload = {
        "symbol": str(data["symbol"]),
        "side": str(data["side"]),
        "quantity": float(data["quantity"]),
        "entry_price": float(data["entry_price"]),
        "state": "OPEN",
        "account_id": int(data["active_account_id"]),
        "trading_session": data.get("trade_session"),
        "strategy_id": data.get("strategy_id"),
        "plan_id": data.get("plan_id"),
        "pre_trade_emotion": data.get("pre_trade_emotion"),
        "risk_reward_ratio": data.get("risk_reward_ratio"),
        "open_timestamp": data.get("trade_open_time")
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/trades",
                json=payload,
                headers={"Authorization": f"Bearer {data.get('access_token')}"},
                timeout=10.0
            )
            if resp.status_code == 201:
                session_display = get_session_display_name(data.get("trade_session", ""))
                
                await state.set_state(None)
                await message.answer(
                    f"✅ <b>Trade Logged!</b>\n"
                    f"{payload['symbol']} {payload['side']} @ {payload['entry_price']}\n"
                    f"Session: {session_display}\n"
                    f"Emotion: {data.get('pre_trade_emotion', 'N/A')}\n"
                    f"R:R: {data.get('risk_reward_ratio', 'N/A')}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = resp.json().get('detail', 'Unknown error')
                await message.answer(f"<b>Error:</b> {detail}", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Trade creation error: {e}")
        await message.answer("Connection failure. Please try again.")


@router.callback_query(F.data == "trade_close")
async def list_trades_for_closing(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("Session missing.", show_alert=True)
         
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        open_trades = [t for t in trades if t['state'] != 'CLOSED']
        if not open_trades:
            return await callback.message.answer("No open trades found.")
            
        btns = [[InlineKeyboardButton(text=f"❌ {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"close_trd_{t['id']}")] for t in open_trades]
        
        await callback.message.edit_text("<b>Select trade to close:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Close list error: {e}")
        await callback.answer("Error fetching trades.")
    await callback.answer()


@router.callback_query(F.data.startswith("close_trd_"))
async def start_close_trade_price(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    await state.update_data(closing_trade_id=trade_id)
    await callback.message.answer(
        f"Closing Trade ID <code>{trade_id}</code>.\nEnter exit price:", 
        reply_markup=get_cancel_action(), 
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_exit_price)
    await callback.answer()


@router.message(TradeStates.waiting_for_exit_price)
async def process_exit_price(message: Message, state: FSMContext):
    try:
        exit_p = float(message.text.strip())
        await state.update_data(exit_price=exit_p)
        
        await message.answer(
            f"Exit: <b>${exit_p}</b>\n\nHow did you feel after this trade?",
            reply_markup=get_emotion_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(TradeStates.waiting_for_post_emotion)
    except ValueError:
        await message.answer("Enter a numeric price:")


@router.callback_query(TradeStates.waiting_for_post_emotion, F.data.startswith("emotion:"))
async def process_post_emotion(callback: CallbackQuery, state: FSMContext):
    emotion = callback.data.split(":")[1]
    data = await state.get_data()
    trade_id = data.get("closing_trade_id")
    exit_p = data.get("exit_price")
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}",
                json={
                    "exit_price": exit_p, 
                    "state": "CLOSED",
                    "post_trade_emotion": emotion
                },
                headers={"Authorization": f"Bearer {data.get('access_token')}"}
            )
            if resp.status_code == 200:
                trade_result = resp.json()
                pnl = trade_result.get("pnl", 0)
                outcome = trade_result.get("outcome", "")
                
                await state.set_state(None)
                await callback.message.answer(
                    f"✅ <b>Trade Closed!</b>\n"
                    f"P&L: ${pnl:,.2f}\n"
                    f"Outcome: {outcome}\n"
                    f"Post-trade emotion: {emotion}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer("Error closing trade.")
    except Exception as e:
        logger.error(f"Trade close error: {e}")
        await callback.message.answer("Connection failure.")
    await callback.answer()


@router.callback_query(F.data == "trade_modify")
async def list_trades_for_modification(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("Session missing.", show_alert=True)
         
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        open_trades = [t for t in trades if t['state'] != 'CLOSED']
        if not open_trades:
            return await callback.message.answer("No open trades found to modify.")
            
        btns = [[InlineKeyboardButton(text=f"📝 {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"mod_trd_{t['id']}")] for t in open_trades]
        await callback.message.edit_text("<b>Select trade to modify:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Modify list error: {e}")
        await callback.answer("Error.")
    await callback.answer()


@router.callback_query(F.data.startswith("mod_trd_"))
async def select_field_to_modify(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    await state.update_data(modifying_trade_id=trade_id)
    await callback.message.edit_text(
        f"<b>Modifying Trade ID {trade_id}</b>\nWhat would you like to update?", 
        reply_markup=ik.get_modify_field_options(), 
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_field_selection)
    await callback.answer()


@router.callback_query(TradeStates.waiting_for_field_selection, F.data.startswith("mod_field_"))
async def prompt_for_new_value(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace("mod_field_", "")
    await state.update_data(modifying_field=field)
    label = "New Lot Size" if field == "quantity" else "New Entry Price"
    await callback.message.answer(f"Enter the <b>{label}</b>:", reply_markup=get_cancel_action(), parse_mode="HTML")
    await state.set_state(TradeStates.waiting_for_new_value)
    await callback.answer()


@router.message(TradeStates.waiting_for_new_value)
async def process_modified_value(message: Message, state: FSMContext):
    try:
        new_val = float(message.text.strip())
        data = await state.get_data() or {}
        trade_id, field = data.get("modifying_trade_id"), data.get("modifying_field")
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}", 
                json={field: new_val}, 
                headers={"Authorization": f"Bearer {data.get('access_token')}"}
            )
            if resp.status_code == 200:
                await state.set_state(None)
                await message.answer("✅ Trade updated!", reply_markup=get_main_menu())
    except ValueError:
        await message.answer("Enter a number:")


@router.callback_query(F.data == "trade_delete")
async def list_trades_for_deletion(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("Session missing.", show_alert=True)
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found.")
        btns = [[InlineKeyboardButton(text=f"🗑️ {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"del_trd_{t['id']}")] for t in trades]
        await callback.message.edit_text("<b>Select trade to delete:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Delete list error: {e}")
        await callback.answer("Error.")
    await callback.answer()


@router.callback_query(F.data.startswith("del_trd_"))
async def process_trade_deletion(callback: CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    auth = (await state.get_data() or {}).get("access_token")
    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}", 
            headers={"Authorization": f"Bearer {auth}"}
        )
        if res.status_code == 204:
            await callback.message.edit_text(
                "✅ Trade deleted.", 
                reply_markup=ik.get_trade_management(), 
                parse_mode="HTML"
            )
    await callback.answer()
