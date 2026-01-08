import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.database import SessionLocal
from app.services.analytics_service import (
    recalculate_user_stats,
    get_user_stats,
    format_stats_overview,
    format_session_comparison,
    get_strategy_performance,
    get_hourly_performance,
    get_win_rate
)
from app.utils.streak_utils import format_streak_display
from app.telegram.utils.auth import get_user_id_from_state

logger = logging.getLogger(__name__)
router = Router()


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


@router.message(F.text == "📈 Stats")
async def menu_stats(message: Message, state):
    """Handler for main menu Stats button."""
    await cmd_stats(message, state)


@router.message(Command("stats"))
async def cmd_stats(message: Message, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await message.answer("Please /login first.")
        return
    
    db = SessionLocal()
    try:
        stats = recalculate_user_stats(db, user_id)
        overview = format_stats_overview(stats)
        
        await message.answer(
            f"<b>Your Trading Statistics</b>\n\n{overview}",
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    finally:
        db.close()


@router.callback_query(F.data == "stats:overview")
async def cb_stats_overview(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        stats = get_user_stats(db, user_id)
        if not stats:
            await callback.answer("No stats yet. Close some trades first.", show_alert=True)
            return
        
        overview = format_stats_overview(stats)
        await callback.message.edit_text(
            f"<b>Trading Overview</b>\n\n{overview}",
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "stats:sessions")
async def cb_stats_sessions(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        stats = get_user_stats(db, user_id)
        if not stats:
            await callback.answer("No stats yet.", show_alert=True)
            return
        
        london_total = stats.london_wins + stats.london_losses
        ny_total = stats.newyork_wins + stats.newyork_losses
        asian_total = stats.asian_wins + stats.asian_losses
        sydney_total = stats.sydney_wins + stats.sydney_losses
        
        lines = ["<b>Session Performance</b>\n"]
        
        if london_total > 0:
            london_wr = round((stats.london_wins / london_total) * 100, 1)
            lines.append(f"London: {london_wr}% ({stats.london_wins}W / {stats.london_losses}L)")
        
        if ny_total > 0:
            ny_wr = round((stats.newyork_wins / ny_total) * 100, 1)
            lines.append(f"New York: {ny_wr}% ({stats.newyork_wins}W / {stats.newyork_losses}L)")
        
        if asian_total > 0:
            asian_wr = round((stats.asian_wins / asian_total) * 100, 1)
            lines.append(f"Asian: {asian_wr}% ({stats.asian_wins}W / {stats.asian_losses}L)")
        
        if sydney_total > 0:
            sydney_wr = round((stats.sydney_wins / sydney_total) * 100, 1)
            lines.append(f"Sydney: {sydney_wr}% ({stats.sydney_wins}W / {stats.sydney_losses}L)")
        
        if len(lines) == 1:
            lines.append("No session data yet. Close some trades to see performance by session.")
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "stats:strategies")
async def cb_stats_strategies(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        performance = get_strategy_performance(db, user_id)
        
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
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "stats:time")
async def cb_stats_time(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        hourly = get_hourly_performance(db, user_id)
        
        best_hours = []
        for hour, data in hourly.items():
            total = data["wins"] + data["losses"]
            if total >= 2:
                wr = (data["wins"] / total) * 100
                best_hours.append((hour, wr, data["wins"], data["losses"]))
        
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
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "stats:streak")
async def cb_stats_streak(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        stats = get_user_stats(db, user_id)
        if not stats:
            await callback.answer("No stats yet.", show_alert=True)
            return
        
        streak_display = format_streak_display(stats.current_streak, stats.current_streak_type)
        
        lines = [
            "<b>Streak Tracking</b>\n",
            f"Current: {streak_display}",
            f"Best Win Streak: {stats.best_win_streak}",
            f"Worst Loss Streak: {stats.worst_loss_streak}"
        ]
        
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
    finally:
        db.close()
    await callback.answer()


@router.callback_query(F.data == "stats:refresh")
async def cb_stats_refresh(callback: CallbackQuery, state):
    user_id = await get_user_id_from_state(state)
    if not user_id:
        await callback.answer("Please /login first.", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        stats = recalculate_user_stats(db, user_id)
        overview = format_stats_overview(stats)
        
        await callback.message.edit_text(
            f"<b>Your Trading Statistics</b> (Refreshed)\n\n{overview}",
            reply_markup=get_stats_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("Stats refreshed!")
    finally:
        db.close()
