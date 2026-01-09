import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User
from app.services.analytics_service import get_user_stats, get_win_rate, get_day_of_week_performance

logger = logging.getLogger(__name__)


def generate_weekly_summary(db: Session, user_id: int) -> str:
    stats = get_user_stats(db, user_id)
    
    if not stats:
        return None
    
    days = get_day_of_week_performance(db, user_id)
    win_rate = get_win_rate(stats)
    
    lines = ["<b>Weekly Trading Summary</b>\n"]
    lines.append(f"Trades: {stats.total_trades}")
    lines.append(f"Win Rate: {win_rate}%")
    lines.append(f"P&L: ${stats.total_pnl:,.2f}")
    lines.append(f"Wins: {stats.winning_trades} | Losses: {stats.losing_trades}")
    
    if days:
        best_day = max(days.items(), key=lambda x: x[1]["win_rate"])
        worst_day = min(days.items(), key=lambda x: x[1]["win_rate"])
        lines.append(f"\nBest Day: {best_day[0]} ({best_day[1]['win_rate']}%)")
        lines.append(f"Worst Day: {worst_day[0]} ({worst_day[1]['win_rate']}%)")
    
    if stats.current_streak > 0:
        lines.append(f"\nCurrent Streak: {stats.current_streak} {stats.current_streak_type}")
    
    lines.append("\nKeep up the good work!")
    
    return "\n".join(lines)


async def send_weekly_summaries(bot):
    logger.info("Sending weekly summaries...")
    
    db = SessionLocal()
    try:
        users_stmt = select(User)
        users = db.scalars(users_stmt).all()
        
        for user in users:
            if user.telegram_id:
                try:
                    summary = generate_weekly_summary(db, user.id)
                    if summary:
                        await bot.send_message(
                            chat_id=user.telegram_id,
                            text=summary,
                            parse_mode="HTML"
                        )
                        logger.info(f"Sent weekly summary to user {user.id}")
                except Exception as e:
                    logger.error(f"Failed to send summary to user {user.id}: {e}")
    except Exception as e:
        logger.error(f"Weekly summary job failed: {e}")
    finally:
        db.close()


def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        send_weekly_summaries,
        trigger=CronTrigger(day_of_week="sun", hour=20, minute=0),
        args=[bot],
        id="weekly_summary",
        name="Send weekly trading summaries",
        replace_existing=True
    )
    
    return scheduler
