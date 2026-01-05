import logging
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.activity import Activity
from datetime import date

# Rule 10: Observability
logger = logging.getLogger(__name__)

MAX_ACTIVITY_TYPES_PER_DAY = 10

def log_activity(db: Session, user_id: int, activity_date: date, activity_type: str) -> Activity:
    """Rule 5: Idempotent logging. Rule 12: Explicit error handling."""
    try:
        # Check for existing record (Idempotency)
        existing_stmt = select(Activity).where(
            and_(
                Activity.user_id == user_id,
                Activity.date == activity_date,
                Activity.activity_type == activity_type
            )
        )
        existing = db.execute(existing_stmt).scalars().first()
        if existing:
            return existing

        # Rule 6: No guessing - check limits explicitly
        count_stmt = select(func.count(Activity.id)).where(
            Activity.user_id == user_id,
            Activity.date == activity_date
        )
        count = db.execute(count_stmt).scalar() or 0

        if count >= MAX_ACTIVITY_TYPES_PER_DAY:
            raise ValueError("MAX_ACTIVITY_LOGS_REACHED")

        activity = Activity(user_id=user_id, date=activity_date, activity_type=activity_type)
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    except SQLAlchemyError as e:
        db.rollback() # Rule 7: Recovery from failure
        logger.error(f"Database error logging activity: {e}")
        raise RuntimeError("DATABASE_TRANSACTION_FAILED")

def list_activities(db: Session, user_id: int, activity_date: date = None):
    """Rule 13: Consistent 2.0 style queries."""
    stmt = select(Activity).where(Activity.user_id == user_id)
    if activity_date:
        stmt = stmt.where(Activity.date == activity_date)
    
    return db.execute(stmt.order_by(desc(Activity.date))).scalars().all()

def get_activity(db: Session, activity_id: int):
    return db.get(Activity, activity_id)

def delete_activity(db: Session, activity_id: int) -> bool:
    try:
        activity = get_activity(db, activity_id)
        if not activity:
            return False
        db.delete(activity)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
