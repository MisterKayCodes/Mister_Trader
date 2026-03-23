import logging
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.voice_note import VoiceNote

logger = logging.getLogger(__name__)

def create_voice_note(db: Session, user_id: int, trade_id: int, file_path: str, trade_state_at_time: str) -> VoiceNote:
    try:
        # Rule 1: Link record to the authenticated user_id
        note = VoiceNote(
            user_id=user_id,
            trade_id=trade_id,
            file_path=file_path,
            trade_state_at_time=trade_state_at_time
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create VoiceNote for trade {trade_id}: {e}")
        raise RuntimeError("Failed to create voice note.")

def list_voice_notes(db: Session, trade_id: int, user_id: int):
    # Rule 14: Filter by user_id to prevent data leaking
    stmt = select(VoiceNote).where(and_(VoiceNote.trade_id == trade_id, VoiceNote.user_id == user_id))
    return db.execute(stmt).scalars().all()

def get_voice_note(db: Session, note_id: int, user_id: int):
    # Rule 6: Explicitly find the note belonging to this specific user
    stmt = select(VoiceNote).where(and_(VoiceNote.id == note_id, VoiceNote.user_id == user_id))
    return db.execute(stmt).scalars().first()

def update_voice_note(db: Session, note_id: int, user_id: int, file_path: str | None = None, trade_state_at_time: str | None = None):
    note = get_voice_note(db, note_id, user_id)
    if not note:
        return None
    if file_path is not None:
        note.file_path = file_path
    if trade_state_at_time is not None:
        note.trade_state_at_time = trade_state_at_time
    try:
        db.commit()
        db.refresh(note)
        return note
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update VoiceNote {note_id}: {e}")
        return None

def delete_voice_note(db: Session, note_id: int, user_id: int) -> bool:
    note = get_voice_note(db, note_id, user_id)
    if not note:
        return False
    file_path = note.file_path
    
    try:
        db.delete(note)
        db.commit()
        
        # Rule 2: Delete from disk only after successful DB commit
        if file_path:
            from app.core.storage import delete_file
            delete_file(file_path)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete VoiceNote {note_id}: {e}")
        return False
