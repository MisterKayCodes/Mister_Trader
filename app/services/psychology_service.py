import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.trade_psychology import TradePsychology
from app.schemas.psychology import TradePsychologyUpdate

logger = logging.getLogger(__name__)


def create_trade_psychology(
    db: Session,
    trade_id: int,
    discipline,
    confidence,
    followed_plan: bool,
    notes: str | None = None,
) -> TradePsychology:
    """
    Rule 5: Idempotent creation.
    One psychology record per trade.
    """
    try:
        # Idempotency: return existing record if already created
        existing = (
            db.query(TradePsychology)
            .filter(TradePsychology.trade_id == trade_id)
            .first()
        )
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
        logger.error(
            f"Failed to create TradePsychology for trade {trade_id}: {e}"
        )
        raise RuntimeError("FAILED_TO_CREATE_TRADE_PSYCHOLOGY") from e


def get_trade_psychology(db: Session, psychology_id: int):
    """
    Fetch psychology by ID.
    """
    return (
        db.query(TradePsychology)
        .filter(TradePsychology.id == psychology_id)
        .first()
    )


def get_trade_psychology_by_trade(db: Session, trade_id: int):
    """
    Fetch psychology for a specific trade.
    """
    return (
        db.query(TradePsychology)
        .filter(TradePsychology.trade_id == trade_id)
        .first()
    )


def update_trade_psychology(
    db: Session,
    psychology_id: int,
    update: TradePsychologyUpdate,
):
    """
    Partial update. Only provided fields are updated.
    """
    try:
        psychology = get_trade_psychology(db, psychology_id)
        if not psychology:
            return None

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
        logger.error(
            f"Failed to update TradePsychology {psychology_id}: {e}"
        )
        raise RuntimeError("FAILED_TO_UPDATE_TRADE_PSYCHOLOGY") from e


def delete_trade_psychology(db: Session, psychology_id: int) -> bool:
    """
    Explicit delete with state safety.
    """
    try:
        psychology = get_trade_psychology(db, psychology_id)
        if not psychology:
            return False

        db.delete(psychology)
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"Failed to delete TradePsychology {psychology_id}: {e}"
        )
        return False
