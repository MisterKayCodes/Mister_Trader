import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.voice_note import VoiceNote

logger = logging.getLogger(__name__)

def create_voice_note(db: Session, trade_id: int, file_path: str, trade_state_at_time) -> VoiceNote:
    try:
        note = VoiceNote(
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

def list_voice_notes(db: Session, trade_id: int):
    return db.query(VoiceNote).filter(VoiceNote.trade_id == trade_id).all()

def get_voice_note(db: Session, note_id: int):
    return db.query(VoiceNote).filter(VoiceNote.id == note_id).first()

def update_voice_note(db: Session, note_id: int, file_path: str | None = None, trade_state_at_time = None):
    note = get_voice_note(db, note_id)
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

def delete_voice_note(db: Session, note_id: int) -> bool:
    note = get_voice_note(db, note_id)
    if not note:
        return False
    try:
        db.delete(note)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete VoiceNote {note_id}: {e}")
        return False
