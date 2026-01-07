from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_pin, verify_pin

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.execute(select(User).where(User.telegram_user_id == telegram_id)).scalars().first()

def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)

def create_user(db: Session, user_in: UserCreate):
    # Rule 14: Hash the PIN before it ever touches the DB
    db_user = User(
        telegram_user_id=user_in.telegram_user_id,
        hashed_pin=hash_pin(user_in.pin)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, telegram_id: int, pin: str):
    user = get_user_by_telegram_id(db, telegram_id)
    if not user or not verify_pin(pin, user.hashed_pin):
        return None
    return user
