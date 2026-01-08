from datetime import date
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import Session
from app.models.activity import Activity

def log_activity(db: Session, user_id: int, activity_date: date, activity_type: str) -> Activity:
    stmt = select(Activity).where(
        and_(Activity.user_id == user_id, Activity.date == activity_date, Activity.activity_type == activity_type)
    )
    existing = db.scalar(stmt)
    if existing:
        return existing

    count_stmt = select(func.count(Activity.id)).where(Activity.user_id == user_id, Activity.date == activity_date)
    count = db.scalar(count_stmt) or 0
    if count >= 10:
        raise ValueError("MAX_ACTIVITY_LOGS_REACHED")

    activity = Activity(user_id=user_id, date=activity_date, activity_type=activity_type)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def get_activity_secure(db: Session, activity_id: int, user_id: int):
    """Rule 14: Never fetch an activity without verifying the owner."""
    stmt = select(Activity).where(and_(Activity.id == activity_id, Activity.user_id == user_id))
    return db.scalar(stmt)

def delete_activity_secure(db: Session, activity_id: int, user_id: int) -> bool:
    activity = get_activity_secure(db, activity_id, user_id)
    if not activity:
        return False
    db.delete(activity)
    db.commit()
    return True

def list_activities(db: Session, user_id: int, activity_date: date = None):
    """Rule 14: Return only activities belonging to the user."""
    if activity_date:
        stmt = select(Activity).where(
            and_(Activity.user_id == user_id, Activity.date == activity_date)
        ).order_by(desc(Activity.date))
    else:
        stmt = select(Activity).where(
            Activity.user_id == user_id
        ).order_by(desc(Activity.date)).limit(50)
    return db.scalars(stmt).all()
