import logging
from datetime import time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from app.models.reminder import Reminder

logger = logging.getLogger(__name__)

REMINDER_TYPES = {
    "session_london": "London Session Alert",
    "session_newyork": "New York Session Alert",
    "session_asian": "Asian Session Alert",
    "trading_plan": "Daily Trading Plan Reminder",
    "journal_prompt": "Post-Trade Journal Prompt",
    "weekly_review": "Weekly Performance Review"
}


def create_reminder(
    db: Session,
    user_id: int,
    reminder_type: str,
    time_utc: time = None,
    days_of_week: str = None,
    message: str = None
) -> Reminder:
    try:
        reminder = Reminder(
            user_id=user_id,
            reminder_type=reminder_type,
            time_utc=time_utc,
            days_of_week=days_of_week,
            message=message
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create reminder: {e}")
        raise RuntimeError("DATABASE_ERROR")


def get_reminder(db: Session, user_id: int, reminder_id: int) -> Optional[Reminder]:
    stmt = select(Reminder).where(
        and_(Reminder.id == reminder_id, Reminder.user_id == user_id)
    )
    return db.scalar(stmt)


def list_reminders(db: Session, user_id: int, enabled_only: bool = False) -> List[Reminder]:
    stmt = select(Reminder).where(Reminder.user_id == user_id)
    if enabled_only:
        stmt = stmt.where(Reminder.is_enabled == True)
    return list(db.scalars(stmt).all())


def toggle_reminder(db: Session, user_id: int, reminder_id: int) -> Optional[Reminder]:
    reminder = get_reminder(db, user_id, reminder_id)
    if not reminder:
        return None
    
    reminder.is_enabled = not reminder.is_enabled
    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, user_id: int, reminder_id: int) -> bool:
    reminder = get_reminder(db, user_id, reminder_id)
    if not reminder:
        return False
    
    db.delete(reminder)
    db.commit()
    return True


def get_or_create_default_reminders(db: Session, user_id: int) -> List[Reminder]:
    existing = list_reminders(db, user_id)
    if existing:
        return existing
    
    defaults = [
        ("session_london", time(6, 30), "0,1,2,3,4"),
        ("session_newyork", time(11, 30), "0,1,2,3,4"),
        ("trading_plan", time(6, 0), "0,1,2,3,4"),
        ("weekly_review", time(18, 0), "4"),
    ]
    
    reminders = []
    for r_type, r_time, days in defaults:
        reminder = Reminder(
            user_id=user_id,
            reminder_type=r_type,
            time_utc=r_time,
            days_of_week=days,
            is_enabled=False
        )
        db.add(reminder)
        reminders.append(reminder)
    
    db.commit()
    return reminders


def format_reminder_list(reminders: List[Reminder]) -> str:
    if not reminders:
        return "No reminders configured."
    
    lines = []
    for r in reminders:
        status = "ON" if r.is_enabled else "OFF"
        name = REMINDER_TYPES.get(r.reminder_type, r.reminder_type)
        time_str = r.time_utc.strftime("%H:%M") if r.time_utc else "Not set"
        lines.append(f"[{status}] {name} - {time_str} UTC")
    
    return "\n".join(lines)
