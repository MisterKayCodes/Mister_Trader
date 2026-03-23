import os
import httpx
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.telegram.keyboards.reply_keyboards import get_main_menu

logger = logging.getLogger(__name__)
router = Router()
<<<<<<< HEAD
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
=======
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:5000")
>>>>>>> 9e6925a (Syncing latest local changes for deployment)


class StrategyStates(StatesGroup):
    waiting_name = State()
    waiting_description = State()
    waiting_entry = State()
    waiting_exit = State()
    waiting_risk = State()


def get_strategy_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="View All", callback_data="strategy:list")
    builder.button(text="+ New Strategy", callback_data="strategy:new")
    builder.adjust(2)
    return builder.as_markup()


def get_strategy_list_keyboard(strategies):
    builder = InlineKeyboardBuilder()
    for s in strategies[:10]:
        status = "Active" if s.get("is_active", True) else "Inactive"
        builder.button(text=f"{s['name']} ({status})", callback_data=f"strategy:view:{s['id']}")
    builder.button(text="Back", callback_data="strategy:menu")
    builder.adjust(1)
    return builder.as_markup()


def get_strategy_detail_keyboard(strategy_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Delete", callback_data=f"strategy:delete:{strategy_id}")
    builder.button(text="Back to List", callback_data="strategy:list")
    builder.adjust(2)
    return builder.as_markup()


@router.message(F.text == "📋 Strategies")
async def menu_strategy(message: Message, state: FSMContext):
    await cmd_strategy(message, state)


@router.message(Command("strategy"))
async def cmd_strategy(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await message.answer("Please /login first.")
        return
    
    await message.answer(
        "<b>Strategy Manager</b>\n\nCreate and manage your trading strategies. Link them to trades to track their performance.",
        reply_markup=get_strategy_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "strategy:menu")
async def cb_strategy_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Strategy Manager</b>\n\nCreate and manage your trading strategies.",
        reply_markup=get_strategy_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "strategy:list")
async def cb_strategy_list(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/strategies/",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            strategies = response.json()
        
        if not strategies:
            await callback.message.edit_text(
                "<b>No Strategies Yet</b>\n\nCreate your first trading strategy to start tracking performance.",
                reply_markup=get_strategy_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                f"<b>Your Strategies</b> ({len(strategies)} total)\n\nSelect a strategy to view details:",
                reply_markup=get_strategy_list_keyboard(strategies),
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Strategy list error: {e}")
        await callback.answer("Failed to fetch strategies.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data.startswith("strategy:view:"))
async def cb_strategy_view(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    strategy_id = int(callback.data.split(":")[2])
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/strategies/{strategy_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            strategy = response.json()
        
        lines = [f"<b>{strategy['name']}</b>\n"]
        if strategy.get("description"):
            lines.append(f"<i>{strategy['description']}</i>\n")
        if strategy.get("entry_criteria"):
            lines.append(f"Entry: {strategy['entry_criteria']}")
        if strategy.get("exit_criteria"):
            lines.append(f"Exit: {strategy['exit_criteria']}")
        if strategy.get("risk_per_trade"):
            lines.append(f"Risk: {strategy['risk_per_trade']}")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_strategy_detail_keyboard(strategy_id),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Strategy view error: {e}")
        await callback.answer("Strategy not found.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "strategy:new")
async def cb_strategy_new(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not user_data.get("access_token"):
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    await state.set_state(StrategyStates.waiting_name)
    await callback.message.edit_text(
        "<b>Create New Strategy</b>\n\nWhat's the name of this strategy?",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(StrategyStates.waiting_name)
async def process_strategy_name(message: Message, state: FSMContext):
    await state.update_data(strategy_name=message.text)
    await state.set_state(StrategyStates.waiting_description)
    await message.answer("Describe your strategy briefly (or send 'skip'):")


@router.message(StrategyStates.waiting_description)
async def process_strategy_description(message: Message, state: FSMContext):
    desc = message.text if message.text.lower() != "skip" else None
    await state.update_data(strategy_description=desc)
    await state.set_state(StrategyStates.waiting_entry)
    await message.answer("Entry criteria? (or send 'skip'):")


@router.message(StrategyStates.waiting_entry)
async def process_strategy_entry(message: Message, state: FSMContext):
    entry = message.text if message.text.lower() != "skip" else None
    await state.update_data(strategy_entry=entry)
    await state.set_state(StrategyStates.waiting_exit)
    await message.answer("Exit criteria? (or send 'skip'):")


@router.message(StrategyStates.waiting_exit)
async def process_strategy_exit(message: Message, state: FSMContext):
    exit_c = message.text if message.text.lower() != "skip" else None
    await state.update_data(strategy_exit=exit_c)
    await state.set_state(StrategyStates.waiting_risk)
    await message.answer("Risk per trade? (e.g., '1%' or 'skip'):")


@router.message(StrategyStates.waiting_risk)
async def process_strategy_risk(message: Message, state: FSMContext):
    risk = message.text if message.text.lower() != "skip" else None
    
    data = await state.get_data()
    auth_token = data.get("access_token")
    
    if not auth_token:
        await state.set_state(None)
        await message.answer("Session expired. Please /login again.")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/strategies/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "name": data["strategy_name"],
                    "description": data.get("strategy_description"),
                    "entry_criteria": data.get("strategy_entry"),
                    "exit_criteria": data.get("strategy_exit"),
                    "risk_per_trade": risk
                },
                timeout=10.0
            )
            response.raise_for_status()
            strategy = response.json()
        
        await state.set_state(None)
        await message.answer(
            f"Strategy '<b>{strategy['name']}</b>' created successfully!",
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Failed to create strategy: {e}")
        await message.answer("Failed to create strategy. Please try again.")
        await state.set_state(None)


@router.callback_query(F.data.startswith("strategy:delete:"))
async def cb_strategy_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    strategy_id = int(callback.data.split(":")[2])
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{BOT_BACKEND_URL}/api/v1/strategies/{strategy_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
        
        await callback.message.edit_text(
            "Strategy deleted.",
            reply_markup=get_strategy_menu_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("Deleted!")
    except Exception as e:
        logger.error(f"Strategy delete error: {e}")
        await callback.answer("Failed to delete strategy.", show_alert=True)
