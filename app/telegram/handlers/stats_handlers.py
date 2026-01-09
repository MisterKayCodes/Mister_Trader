import os
import httpx
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger(__name__)
router = Router()
BOT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")


def get_stats_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Overview", callback_data="stats:overview")
    builder.button(text="Sessions", callback_data="stats:sessions")
    builder.button(text="Strategies", callback_data="stats:strategies")
    builder.button(text="Time Analysis", callback_data="stats:time")
    builder.button(text="Streak", callback_data="stats:streak")
    builder.button(text="Refresh", callback_data="stats:refresh")
    builder.adjust(2, 2, 2)
    return builder.as_markup()


async def _get_stats(auth_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BOT_BACKEND_URL}/api/v1/analytics/stats/",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()


@router.message(F.text == "📈 Stats")
async def menu_stats(message: Message, state: FSMContext):
    await cmd_stats(message, state)


@router.message(Command("stats"))
async def cmd_stats(message: Message, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await message.answer("Please /login first.")
        return
    
    try:
        stats = await _get_stats(auth_token)
        
        lines = ["<b>Your Trading Statistics</b>\n"]
        lines.append(f"Total Trades: {stats.get('total_trades', 0)}")
        lines.append(f"Win Rate: {stats.get('win_rate', 0):.1f}%")
        lines.append(f"Total P&L: ${stats.get('total_pnl', 0):,.2f}")
        lines.append(f"Wins: {stats.get('total_wins', 0)} | Losses: {stats.get('total_losses', 0)}")
        
        await message.answer(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Stats fetch error: {e}")
        await message.answer("Failed to fetch stats. Please try again.")


@router.callback_query(F.data == "stats:overview")
async def cb_stats_overview(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        stats = await _get_stats(auth_token)
        
        lines = ["<b>Trading Overview</b>\n"]
        lines.append(f"Total Trades: {stats.get('total_trades', 0)}")
        lines.append(f"Win Rate: {stats.get('win_rate', 0):.1f}%")
        lines.append(f"Total P&L: ${stats.get('total_pnl', 0):,.2f}")
        lines.append(f"Wins: {stats.get('total_wins', 0)} | Losses: {stats.get('total_losses', 0)}")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Stats overview error: {e}")
        await callback.answer("Failed to fetch stats.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "stats:sessions")
async def cb_stats_sessions(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        stats = await _get_stats(auth_token)
        sessions = stats.get("sessions", {})
        
        lines = ["<b>Session Performance</b>\n"]
        
        for session_name in ["london", "newyork", "asian", "sydney"]:
            session_data = sessions.get(session_name, {})
            wins = session_data.get("wins", 0)
            losses = session_data.get("losses", 0)
            total = wins + losses
            if total > 0:
                wr = round((wins / total) * 100, 1)
                display_name = session_name.replace("newyork", "New York").title()
                lines.append(f"{display_name}: {wr}% ({wins}W / {losses}L)")
        
        if len(lines) == 1:
            lines.append("No session data yet. Close some trades to see performance by session.")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Stats sessions error: {e}")
        await callback.answer("Failed to fetch session stats.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "stats:strategies")
async def cb_stats_strategies(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/analytics/strategies/",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            performance = response.json()
        
        if not performance:
            await callback.message.edit_text(
                "<b>Strategy Performance</b>\n\nNo strategy data yet. Tag your trades with strategies to see their performance.",
                reply_markup=get_stats_keyboard(),
                parse_mode="HTML"
            )
        else:
            lines = ["<b>Strategy Performance</b>\n"]
            for p in performance[:10]:
                lines.append(f"{p['name']}: {p['win_rate']}% ({p['wins']}W/{p['losses']}L) | P&L: ${p['total_pnl']:,.2f}")
            
            await callback.message.edit_text(
                "\n".join(lines),
                reply_markup=get_stats_keyboard(),
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Stats strategies error: {e}")
        await callback.answer("Failed to fetch strategy stats.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "stats:time")
async def cb_stats_time(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOT_BACKEND_URL}/api/v1/analytics/hourly/",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            hourly = response.json()
        
        best_hours = []
        for hour_str, data in hourly.items():
            total = data["wins"] + data["losses"]
            if total >= 2:
                wr = (data["wins"] / total) * 100
                best_hours.append((int(hour_str), wr, data["wins"], data["losses"]))
        
        best_hours.sort(key=lambda x: x[1], reverse=True)
        
        lines = ["<b>Time Analysis (UTC)</b>\n"]
        
        if best_hours:
            lines.append("Best performing hours:")
            for hour, wr, wins, losses in best_hours[:5]:
                lines.append(f"{hour:02d}:00 - {wr:.0f}% ({wins}W/{losses}L)")
        else:
            lines.append("Not enough data yet. Need at least 2 trades per hour to show analysis.")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Stats time error: {e}")
        await callback.answer("Failed to fetch time stats.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "stats:streak")
async def cb_stats_streak(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        stats = await _get_stats(auth_token)
        
        current_streak = stats.get("current_streak", 0)
        streak_type = stats.get("current_streak_type", "none")
        best_win = stats.get("best_win_streak", 0)
        worst_loss = stats.get("worst_loss_streak", 0)
        
        if streak_type == "win":
            streak_display = f"{current_streak} Wins"
        elif streak_type == "loss":
            streak_display = f"{current_streak} Losses"
        else:
            streak_display = "No streak"
        
        lines = [
            "<b>Streak Tracking</b>\n",
            f"Current: {streak_display}",
            f"Best Win Streak: {best_win}",
            f"Worst Loss Streak: {worst_loss}"
        ]
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Stats streak error: {e}")
        await callback.answer("Failed to fetch streak stats.", show_alert=True)
    await callback.answer()


@router.callback_query(F.data == "stats:refresh")
async def cb_stats_refresh(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data() or {}
    auth_token = user_data.get("access_token")
    
    if not auth_token:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BOT_BACKEND_URL}/api/v1/analytics/refresh/",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            response.raise_for_status()
            stats = response.json()
        
        lines = ["<b>Your Trading Statistics</b> (Refreshed)\n"]
        lines.append(f"Total Trades: {stats.get('total_trades', 0)}")
        lines.append(f"Win Rate: {stats.get('win_rate', 0):.1f}%")
        lines.append(f"Total P&L: ${stats.get('total_pnl', 0):,.2f}")
        lines.append(f"Wins: {stats.get('total_wins', 0)} | Losses: {stats.get('total_losses', 0)}")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("Stats refreshed!")
    except Exception as e:
        logger.error(f"Stats refresh error: {e}")
        await callback.answer("Failed to refresh stats.", show_alert=True)
