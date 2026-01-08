import os
import httpx
import logging
from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.telegram.states.trade_states import TradeStates
from app.telegram.keyboards.reply_keyboards import get_main_menu, get_cancel_action
from app.telegram.keyboards import inline_keyboards as ik

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# --- Helper Functions ---

async def _fetch_user_trades(auth_token: str, account_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/trades?account_id={account_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        response.raise_for_status()
        return response.json()

def _check_active_account(user_data):
    if not user_data.get("access_token") or not user_data.get("active_account_id"):
        return False
    return True

# --- Main Menu Entry ---

@router.message(F.text == "📊 Active Trades")
async def show_trade_menu(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    active_account = user_data.get("active_account_name", "N/A")

    await message.answer(
        f"📊 <b>Trade Management</b>\nActive Vault: <code>{active_account}</code>\n\nMonitor positions or log new entries.",
        reply_markup=ik.get_trade_management(),
        parse_mode="HTML"
    )

# --- View Trades ---

@router.callback_query(F.data == "trade_view")
async def handle_view_trades(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
    
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades:
            return await callback.message.answer("No trades found in this vault.")
        
        msg = f"📝 <b>Trades in Vault: {user_data.get('active_account_name')}</b>\n"
        for t in trades:
            msg += f"• <code>ID {t['id']}</code>: {t['symbol']} {t['side']} @ {t['entry_price']} ({t['state']})\n"
        
        await callback.message.answer(msg, parse_mode="HTML")
    except Exception:
        await callback.answer("❌ Failed to fetch trades.", show_alert=True)
    await callback.answer()

# --- Open Trade Flow ---

@router.callback_query(F.data == "trade_open")
async def start_open_trade(callback: types.CallbackQuery, state: FSMContext):
    if not _check_active_account(await state.get_data() or {}):
        return await callback.answer("❌ Please set an Active Vault first.", show_alert=True)

    await callback.message.answer(
        "📈 <b>Logging New Trade</b>\nEnter asset symbol (e.g. TSLA):",
        reply_markup=get_cancel_action(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_symbol)
    await callback.answer()

@router.message(TradeStates.waiting_for_symbol)
async def process_symbol(message: Message, state: FSMContext):
    await state.update_data(symbol=message.text.strip().upper())
    await message.answer(
        f"Symbol: <code>{message.text.upper()}</code>\nSelect side:",
        reply_markup=ik.get_trade_side_options(),
        parse_mode="HTML"
    )
    await state.set_state(TradeStates.waiting_for_side)

@router.callback_query(TradeStates.waiting_for_side, F.data.startswith("side_"))
async def process_side(callback: types.CallbackQuery, state: FSMContext):
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
            f"Lot Size: <b>{qty}</b> recorded.\nEnter entry price:",
            parse_mode="HTML"
        )
        await state.set_state(TradeStates.waiting_for_entry_price)
    except ValueError:
        await message.answer("❌ Enter a valid number for lot size:")

@router.message(TradeStates.waiting_for_entry_price)
async def process_entry_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip())
        data = await state.get_data() or {}
        
        payload = {
            "symbol": str(data["symbol"]),
            "side": str(data["side"]),
            "quantity": float(data["quantity"]),
            "entry_price": price,
            "account_id": int(data["active_account_id"])
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/trades",
                json=payload,
                headers={"Authorization": f"Bearer {data.get('access_token')}"},
                timeout=10.0
            )
            if resp.status_code == 201:
                await state.set_state(None)
                await message.answer(
                    f"✅ <b>Trade Logged!</b>\n{payload['symbol']} {payload['side']} @ {price}",
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
            else:
                detail = resp.json().get('detail', 'Unknown error')
                await message.answer(f"❌ <b>Backend Error:</b> {detail}", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Trade creation error: {e}")
        await message.answer("❌ Connection failure.")

# --- Close Trade Flow ---

@router.callback_query(F.data == "trade_close")
async def list_trades_for_closing(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data):
        return await callback.answer("❌ Session missing.", show_alert=True)
         
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        open_trades = [t for t in trades if t['state'] != 'closed']
        if not open_trades: return await callback.message.answer("No open trades found.")
            
        btns = [[InlineKeyboardButton(text=f"❌ {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"close_trd_{t['id']}")] for t in open_trades]
        
        await callback.message.edit_text("<b>Select trade to close:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception:
        await callback.answer("❌ Error fetching trades.")
    await callback.answer()

@router.callback_query(F.data.startswith("close_trd_"))
async def start_close_trade_price(callback: types.CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    await state.update_data(closing_trade_id=trade_id)
    await callback.message.answer(f"Closing Trade ID {trade_id}.\nEnter exit price:", reply_markup=get_cancel_action(), parse_mode="HTML")
    await state.set_state(TradeStates.waiting_for_exit_price)
    await callback.answer()

@router.message(TradeStates.waiting_for_exit_price)
async def process_exit_price(message: Message, state: FSMContext):
    try:
        exit_p = float(message.text.strip())
        data = await state.get_data() or {}
        trade_id = data.get("closing_trade_id")
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}",
                json={"exit_price": exit_p, "state": "closed"},
                headers={"Authorization": f"Bearer {data.get('access_token')}"}
            )
            if resp.status_code == 200:
                await state.set_state(None)
                await message.answer("✅ Trade closed!", reply_markup=get_main_menu())
    except ValueError:
        await message.answer("❌ Enter a numeric price:")

# --- Modify Trade Flow ---

@router.callback_query(F.data == "trade_modify")
async def list_trades_for_modification(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data): return await callback.answer("❌ Session missing.", show_alert=True)
         
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        open_trades = [t for t in trades if t['state'] != 'closed']
        if not open_trades: return await callback.message.answer("No open trades found.")
            
        btns = [[InlineKeyboardButton(text=f"📝 {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"mod_trd_{t['id']}")] for t in open_trades]
        await callback.message.edit_text("<b>Select trade to modify:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception: await callback.answer("❌ Error.")
    await callback.answer()

@router.callback_query(F.data.startswith("mod_trd_"))
async def select_field_to_modify(callback: types.CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    await state.update_data(modifying_trade_id=trade_id)
    await callback.message.edit_text(f"<b>Modifying Trade ID {trade_id}</b>\nWhat would you like to update?", 
                                     reply_markup=ik.get_modify_field_options(), parse_mode="HTML")
    await state.set_state(TradeStates.waiting_for_field_selection)
    await callback.answer()

@router.callback_query(TradeStates.waiting_for_field_selection, F.data.startswith("mod_field_"))
async def prompt_for_new_value(callback: types.CallbackQuery, state: FSMContext):
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
            resp = await client.put(f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}", json={field: new_val}, 
                                     headers={"Authorization": f"Bearer {data.get('access_token')}"})
            if resp.status_code == 200:
                await state.set_state(None)
                await message.answer("✅ Trade updated!", reply_markup=get_main_menu())
    except ValueError: await message.answer("❌ Enter a number:")

# --- Delete Trade Flow ---

@router.callback_query(F.data == "trade_delete")
async def list_trades_for_deletion(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not _check_active_account(user_data): return await callback.answer("❌ Session missing.", show_alert=True)
    try:
        trades = await _fetch_user_trades(user_data["access_token"], user_data["active_account_id"])
        if not trades: return await callback.message.answer("No trades found.")
        btns = [[InlineKeyboardButton(text=f"🗑️ {t['symbol']} @ {t['entry_price']}", 
                callback_data=f"del_trd_{t['id']}")] for t in trades]
        await callback.message.edit_text("<b>Select trade to delete:</b>", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    except Exception: await callback.answer("❌ Error.")
    await callback.answer()

@router.callback_query(F.data.startswith("del_trd_"))
async def process_trade_deletion(callback: types.CallbackQuery, state: FSMContext):
    trade_id = callback.data.split("_")[2]
    auth = (await state.get_data() or {}).get("access_token")
    async with httpx.AsyncClient() as client:
        res = await client.delete(f"{BOT_BACKEND_URL}/api/v1/trades/{trade_id}", headers={"Authorization": f"Bearer {auth}"})
        if res.status_code == 204:
            await callback.message.edit_text("✅ Trade deleted.", reply_markup=ik.get_trade_management(), parse_mode="HTML")
    await callback.answer()
