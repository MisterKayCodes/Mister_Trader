import os
import httpx
import logging
from datetime import date
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.telegram.keyboards.reply_keyboards import get_main_menu

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")


class PlanStates(StatesGroup):
    waiting_title = State()
    waiting_bias = State()
    waiting_watchlist = State()
    waiting_levels = State()
    waiting_mental = State()
    waiting_max_trades = State()
    waiting_notes = State()


def get_plan_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Today's Plan", callback_data="plan:today")
    builder.button(text="View All", callback_data="plan:list")
    builder.button(text="+ New Plan", callback_data="plan:new")
    builder.adjust(2, 1)
    return builder.as_markup()


def get_plan_list_keyboard(plans):
    builder = InlineKeyboardBuilder()
    for p in plans[:10]:
        builder.button(text=f"{p['title']} ({p['plan_date']})", callback_data=f"plan:view:{p['id']}")
    builder.button(text="Back", callback_data="plan:menu")
    builder.adjust(1)
    return builder.as_markup()


def get_plan_detail_keyboard(plan_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Delete", callback_data=f"plan:delete:{plan_id}")
    builder.button(text="Back to List", callback_data="plan:list")
    builder.adjust(2)
    return builder.as_markup()


@router.message(F.text == "📅 Plans")
async def menu_plan(message: Message, state: FSMContext):
    await cmd_plan(message, state)


@router.message(Command("plan"))
async def cmd_plan(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await message.answer("Please /login first.")
        return
    
    await message.answer(
        "<b>Trading Plan Manager</b>\n\nCreate your daily trading plan before the session starts. Review your bias, watchlist, and mental state.",
        reply_markup=get_plan_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "plan:menu")
async def cb_plan_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Trading Plan Manager</b>\n\nCreate and review your trading plans.",
        reply_markup=get_plan_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "plan:today")
async def cb_plan_today(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/plans/today",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            
            if response.status_code == 404:
                await callback.message.edit_text(
                    f"<b>No Plan for Today ({date.today()})</b>\n\nCreate a trading plan before you start trading!",
                    reply_markup=get_plan_menu_keyboard(),
                    parse_mode="HTML"
                )
            else:
                response.raise_for_status()
                plan = response.json()
                
                lines = [f"<b>{plan['title']}</b>", f"Date: {plan['plan_date']}\n"]
                if plan.get("market_bias"):
                    lines.append(f"Bias: {plan['market_bias']}")
                if plan.get("watchlist"):
                    lines.append(f"Watchlist: {plan['watchlist']}")
                if plan.get("key_levels"):
                    lines.append(f"Key Levels: {plan['key_levels']}")
                if plan.get("mental_state"):
                    lines.append(f"Mental State: {plan['mental_state']}")
                if plan.get("max_trades"):
                    lines.append(f"Max Trades: {plan['max_trades']}")
                if plan.get("notes"):
                    lines.append(f"\nNotes: {plan['notes']}")
                
                await callback.message.edit_text(
                    "\n".join(lines),
                    reply_markup=get_plan_detail_keyboard(plan['id']),
                    parse_mode="HTML"
                )
    except Exception as e:
        logger.error(f"Plan today error: {e}")
        await callback.answer("Failed to fetch today's plan.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "plan:list")
async def cb_plan_list(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/plans/",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            plans = response.json()
        
        if not plans:
            await callback.message.edit_text(
                "<b>No Trading Plans Yet</b>\n\nCreate your first plan to start building consistency.",
                reply_markup=get_plan_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                f"<b>Recent Trading Plans</b> ({len(plans)} shown)\n\nSelect a plan to view:",
                reply_markup=get_plan_list_keyboard(plans),
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Plan list error: {e}")
        await callback.answer("Failed to fetch plans.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data.startswith("plan:view:"))
async def cb_plan_view(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    plan_id = int(callback.data.split(":")[2])
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/plans/{plan_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            plan = response.json()
        
        lines = [f"<b>{plan['title']}</b>", f"Date: {plan['plan_date']}\n"]
        if plan.get("market_bias"):
            lines.append(f"Bias: {plan['market_bias']}")
        if plan.get("watchlist"):
            lines.append(f"Watchlist: {plan['watchlist']}")
        if plan.get("key_levels"):
            lines.append(f"Key Levels: {plan['key_levels']}")
        if plan.get("mental_state"):
            lines.append(f"Mental State: {plan['mental_state']}")
        if plan.get("max_trades"):
            lines.append(f"Max Trades: {plan['max_trades']}")
        if plan.get("notes"):
            lines.append(f"\nNotes: {plan['notes']}")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_plan_detail_keyboard(plan_id),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Plan view error: {e}")
        await callback.answer("Plan not found.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "plan:new")
async def cb_plan_new(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    if not user_data.get("access_token"):
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    await state.set_state(PlanStates.waiting_title)
    await callback.message.edit_text(
        f"<b>Create Trading Plan for {date.today()}</b>\n\nGive this plan a title:",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(PlanStates.waiting_title)
async def process_plan_title(message: Message, state: FSMContext):
    await state.update_data(plan_title=message.text)
    await state.set_state(PlanStates.waiting_bias)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Bullish", callback_data="bias:BULLISH")
    builder.button(text="Bearish", callback_data="bias:BEARISH")
    builder.button(text="Neutral", callback_data="bias:NEUTRAL")
    builder.adjust(3)
    
    await message.answer("What's your market bias today?", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("bias:"))
async def process_plan_bias(callback: CallbackQuery, state: FSMContext):
    bias = callback.data.split(":")[1]
    await state.update_data(plan_bias=bias)
    await state.set_state(PlanStates.waiting_watchlist)
    await callback.message.edit_text("What pairs/symbols are on your watchlist today? (comma separated or 'skip'):")
    await callback.answer()


@router.message(PlanStates.waiting_watchlist)
async def process_plan_watchlist(message: Message, state: FSMContext):
    watchlist = message.text if message.text.lower() != "skip" else None
    await state.update_data(plan_watchlist=watchlist)
    await state.set_state(PlanStates.waiting_levels)
    await message.answer("Key levels to watch? (or 'skip'):")


@router.message(PlanStates.waiting_levels)
async def process_plan_levels(message: Message, state: FSMContext):
    levels = message.text if message.text.lower() != "skip" else None
    await state.update_data(plan_levels=levels)
    await state.set_state(PlanStates.waiting_mental)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Focused", callback_data="mental:Focused")
    builder.button(text="Calm", callback_data="mental:Calm")
    builder.button(text="Anxious", callback_data="mental:Anxious")
    builder.button(text="Tired", callback_data="mental:Tired")
    builder.button(text="Skip", callback_data="mental:skip")
    builder.adjust(2, 2, 1)
    
    await message.answer("How's your mental state?", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("mental:"))
async def process_plan_mental(callback: CallbackQuery, state: FSMContext):
    mental = callback.data.split(":")[1]
    if mental != "skip":
        await state.update_data(plan_mental=mental)
    await state.set_state(PlanStates.waiting_max_trades)
    await callback.message.edit_text("Maximum trades for today? (number or 'skip'):")
    await callback.answer()


@router.message(PlanStates.waiting_max_trades)
async def process_plan_max_trades(message: Message, state: FSMContext):
    max_trades = None
    if message.text.lower() != "skip":
        try:
            max_trades = int(message.text)
        except ValueError:
            pass
    await state.update_data(plan_max_trades=max_trades)
    await state.set_state(PlanStates.waiting_notes)
    await message.answer("Any additional notes? (or 'skip'):")


@router.message(PlanStates.waiting_notes)
async def process_plan_notes(message: Message, state: FSMContext):
    notes = message.text if message.text.lower() != "skip" else None
    
    data = await state.get_data()
    auth_token = data.get("access_token")
    
    if not auth_token:
        await state.set_state(None)
        await message.answer("Session expired. Please /login again.")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/plans/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "title": data["plan_title"],
                    "plan_date": str(date.today()),
                    "market_bias": data.get("plan_bias"),
                    "watchlist": data.get("plan_watchlist"),
                    "key_levels": data.get("plan_levels"),
                    "mental_state": data.get("plan_mental"),
                    "max_trades": data.get("plan_max_trades"),
                    "notes": notes
                },
                timeout=10.0
            )
            response.raise_for_status()
            plan = response.json()
        
        await state.set_state(None)
        await message.answer(
            f"Trading plan '<b>{plan['title']}</b>' created!\n\nGood luck today!",
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Failed to create plan: {e}")
        await message.answer("Failed to create plan. Please try again.")
        await state.set_state(None)


@router.callback_query(F.data.startswith("plan:delete:"))
async def cb_plan_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    plan_id = int(callback.data.split(":")[2])
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{BOT_BACKEND_URL}/api/v1/plans/{plan_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
        
        await callback.message.edit_text(
            "Plan deleted.",
            reply_markup=get_plan_menu_keyboard()
        )
        await callback.answer("Deleted!")
    except Exception as e:
        logger.error(f"Plan delete error: {e}")
        await callback.answer("Failed to delete plan.", show_alert=True)
