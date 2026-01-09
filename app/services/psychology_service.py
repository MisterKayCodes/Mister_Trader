
import logging
# Import Trade model to verify ownership via user_id
from app.models.trade import Trade 
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from app.models.trade_psychology import TradePsychology
# Using full import path to avoid potential circular imports
from app.schemas.psychology import TradePsychologyUpdate 

logger = logging.getLogger(__name__)

# Helper function to find psychology record with ownership check
def get_psychology_owned_by_user(db: Session, user_id: int, psychology_id: int):
    # Rule 14: Join to Trade model to verify user ownership
    stmt = select(TradePsychology).join(Trade).where(
        and_(TradePsychology.id == psychology_id, Trade.user_id == user_id)
    )
    return db.scalar(stmt)

# Helper function to find psychology by trade ID with ownership check
def get_psychology_by_trade_owned_by_user(db: Session, user_id: int, trade_id: int):
    # Rule 14: Join to Trade model to verify user ownership
    stmt = select(TradePsychology).join(Trade).where(
        and_(TradePsychology.trade_id == trade_id, Trade.user_id == user_id)
    )
    return db.scalar(stmt)


def create_trade_psychology(
    db: Session,
    user_id: int, # <-- Added user_id
    trade_id: int,
    discipline,
    confidence,
    followed_plan: bool,
    notes: str | None = None,
) -> TradePsychology:
    """
    Rule 5 & 14: Idempotent creation with ownership check.
    """
    # Verify the trade belongs to the user before doing anything
    trade_ownership_stmt = select(Trade).where(and_(Trade.id == trade_id, Trade.user_id == user_id))
    user_owns_trade = db.scalar(trade_ownership_stmt)
    if not user_owns_trade:
         raise ValueError("UNAUTHORIZED_TRADE_ACCESS")

    try:
        # Check existing record using the new helper function
        existing = get_psychology_by_trade_owned_by_user(db, user_id, trade_id)
        if existing:
            return existing

        psychology = TradePsychology(
            trade_id=trade_id,
            discipline=discipline,
            confidence=confidence,
            followed_plan=followed_plan,
            notes=notes,
        )
        db.add(psychology)
        db.commit()
        db.refresh(psychology)
        return psychology

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create TradePsychology: {e}")
        raise RuntimeError("DATABASE_ERROR") from e


def get_trade_psychology(db: Session, user_id: int, psychology_id: int):
    """Fetch psychology by ID, ONLY if user owns it."""
    return get_psychology_owned_by_user(db, user_id, psychology_id)


def get_trade_psychology_by_trade(db: Session, user_id: int, trade_id: int):
    """Fetch psychology for a specific trade, ONLY if user owns the trade."""
    return get_psychology_by_trade_owned_by_user(db, user_id, trade_id)


def update_trade_psychology(
    db: Session,
    user_id: int, # <-- Added user_id
    psychology_id: int,
    update: TradePsychologyUpdate,
):
    """
    Rule 14: Verify ownership before allowing a partial update.
    """
    try:
        # Use helper function with ownership check
        psychology = get_psychology_owned_by_user(db, user_id, psychology_id)
        if not psychology:
            return None # 404 handled in router

        # ... (rest of your update logic is good) ...
        if update.discipline is not None:
            psychology.discipline = update.discipline
        if update.confidence is not None:
            psychology.confidence = update.confidence
        if update.followed_plan is not None:
            psychology.followed_plan = update.followed_plan
        if update.notes is not None:
            psychology.notes = update.notes

        db.commit()
        db.refresh(psychology)
        return psychology

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update TradePsychology {psychology_id}: {e}")
        raise RuntimeError("DATABASE_ERROR") from e


def delete_trade_psychology(db: Session, user_id: int, psychology_id: int) -> bool:
    """Rule 14: Ownership check before deletion."""
    try:
        # Use helper function with ownership check
        psychology = get_psychology_owned_by_user(db, user_id, psychology_id)
        if not psychology:
            return False

        db.delete(psychology)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete TradePsychology {psychology_id}: {e}")
        return False

