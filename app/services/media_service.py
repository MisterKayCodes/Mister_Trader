import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.trade_media import TradeMedia

logger = logging.getLogger(__name__)

def create_trade_media(db: Session, trade_id: int, media_type: str, file_path: str) -> TradeMedia:
    """
    Create a new trade media record.
    """
    try:
        media = TradeMedia(trade_id=trade_id, type=media_type, file_path=file_path)
        db.add(media)
        db.commit()
        db.refresh(media)
        return media
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create TradeMedia for trade {trade_id}: {e}")
        raise RuntimeError("Failed to create trade media.")

def list_trade_media(db: Session, trade_id: int):
    """
    List all media associated with a trade.
    """
    return db.query(TradeMedia).filter(TradeMedia.trade_id == trade_id).all()

def get_trade_media(db: Session, media_id: int):
    """
    Get a specific trade media by ID.
    """
    return db.query(TradeMedia).filter(TradeMedia.id == media_id).first()

def delete_trade_media(db: Session, media_id: int) -> bool:
    """
    Delete trade media by ID.
    """
    try:
        media = get_trade_media(db, media_id)
        if not media:
            return False
        db.delete(media)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete TradeMedia {media_id}: {e}")
        return False
