import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.database import SessionLocal
from app.services.strategy_service import (
    create_strategy,
    list_strategies,
    get_strategy,
    delete_strategy,
    format_strategy_summary
)
from app.telegram.utils.auth import get_user_id_from_state

logger = logging.getLogger(__name__)
router = Router()


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
        status = "Active" if s.is_active else "Inactive"
        builder.button(text=f"{s.name} ({status})", callback_data=f"strategy:view:{s.id}")
    builder.button(text="Back", callback_data="strategy:menu")
    builder.adjust(1)
    return builder.as_markup()


def get_strategy_detail_keyboard(strategy_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Delete", callback_data=f"strategy:delete:{strategy_id}")
    builder.button(text="Back to List", callback_data="strategy:list")
    builder.adjust(2)
    return builder.as_markup()


@router.message(Command("strategy"))
async def cmd_strategy(message: Message, state: FSMContext):
    user_id = await get_user_id_from_state(state)
    if not user_id:
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
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        strategies = list_strategies(db, user_id)
        
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
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data.startswith("strategy:view:"))
async def cb_strategy_view(callback: CallbackQuery, state: FSMContext):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    strategy_id = int(callback.data.split(":")[2])
    
    db = SessionLocal()
    try:
        strategy = get_strategy(db, user_id, strategy_id)
        if not strategy:
            await callback.answer("Strategy not found.", show_alert=True)
            return
        
        summary = format_strategy_summary(strategy)
        await callback.message.edit_text(
            summary,
            reply_markup=get_strategy_detail_keyboard(strategy_id),
            parse_mode="HTML"
        )
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "strategy:new")
async def cb_strategy_new(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StrategyStates.waiting_name)
    await callback.message.edit_text(
        "<b>Create New Strategy</b>\n\nWhat's the name of this strategy?",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(StrategyStates.waiting_name)
async def process_strategy_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(StrategyStates.waiting_description)
    await message.answer("Describe your strategy briefly (or send 'skip'):")


@router.message(StrategyStates.waiting_description)
async def process_strategy_description(message: Message, state: FSMContext):
    desc = message.text if message.text.lower() != "skip" else None
    await state.update_data(description=desc)
    await state.set_state(StrategyStates.waiting_entry)
    await message.answer("Entry criteria? (or send 'skip'):")


@router.message(StrategyStates.waiting_entry)
async def process_strategy_entry(message: Message, state: FSMContext):
    entry = message.text if message.text.lower() != "skip" else None
    await state.update_data(entry_criteria=entry)
    await state.set_state(StrategyStates.waiting_exit)
    await message.answer("Exit criteria? (or send 'skip'):")


@router.message(StrategyStates.waiting_exit)
async def process_strategy_exit(message: Message, state: FSMContext):
    exit_c = message.text if message.text.lower() != "skip" else None
    await state.update_data(exit_criteria=exit_c)
    await state.set_state(StrategyStates.waiting_risk)
    await message.answer("Risk per trade? (e.g., '1%' or 'skip'):")


@router.message(StrategyStates.waiting_risk)
async def process_strategy_risk(message: Message, state: FSMContext):
    risk = message.text if message.text.lower() != "skip" else None
    data = await state.get_data()
    await state.clear()
    
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await message.answer("Session expired. Please /login again.")
        return
    
    db = SessionLocal()
    try:
        strategy = create_strategy(
            db,
            user_id=user_id,
            name=data["name"],
            description=data.get("description"),
            entry_criteria=data.get("entry_criteria"),
            exit_criteria=data.get("exit_criteria"),
            risk_per_trade=risk
        )
        
        await message.answer(
            f"Strategy '<b>{strategy.name}</b>' created successfully!",
            reply_markup=get_strategy_menu_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Failed to create strategy: {e}")
        await message.answer("Failed to create strategy. Please try again.")
    finally:
        db.close()


@router.callback_query(F.data.startswith("strategy:delete:"))
async def cb_strategy_delete(callback: CallbackQuery, state: FSMContext):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    strategy_id = int(callback.data.split(":")[2])
    
    db = SessionLocal()
    try:
        if delete_strategy(db, user_id, strategy_id):
            await callback.message.edit_text(
                "Strategy deleted.",
                reply_markup=get_strategy_menu_keyboard(),
                parse_mode="HTML"
            )
            await callback.answer("Deleted!")
        else:
            await callback.answer("Strategy not found.", show_alert=True)
    finally:
        db.close()
