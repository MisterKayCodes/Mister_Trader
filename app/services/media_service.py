import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from app.models.trade_media import TradeMedia
from app.core.storage import delete_file

logger = logging.getLogger(__name__)

def create_trade_media(db: Session, user_id: int, trade_id: int, media_type: str, file_path: str) -> TradeMedia:
    try:
        media = TradeMedia(
            user_id=user_id, 
            trade_id=trade_id, 
            type=media_type, 
            file_path=file_path
        )
        db.add(media)
        db.commit()
        db.refresh(media)
        return media
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create TradeMedia for trade {trade_id}: {e}")
        raise RuntimeError("DATABASE_ERROR")

def list_trade_media(db: Session, user_id: int, trade_id: int):
    stmt = select(TradeMedia).where(
        and_(TradeMedia.user_id == user_id, TradeMedia.trade_id == trade_id)
    )
    return db.scalars(stmt).all()

def get_trade_media(db: Session, user_id: int, media_id: int):
    stmt = select(TradeMedia).where(
        and_(TradeMedia.id == media_id, TradeMedia.user_id == user_id)
    )
    return db.scalar(stmt)

def delete_trade_media(db: Session, user_id: int, media_id: int) -> bool:
    try:
        media = get_trade_media(db, user_id, media_id)
        if not media:
            return False
        
        file_path = media.file_path
        
        db.delete(media)
        db.commit()
        
        if file_path:
            file_deleted = delete_file(file_path)
            if not file_deleted:
                logger.warning(f"Media DB record deleted but file not found: {file_path}")
        
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete TradeMedia {media_id}: {e}")
        return False
