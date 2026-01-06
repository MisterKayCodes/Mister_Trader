from fastapi import APIRouter, HTTPException, Depends, status # Added status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.voice_note import VoiceNoteCreate, VoiceNoteRead, VoiceNoteUpdate
from app.services import voice_note as voice_note_service

router = APIRouter(tags=["voice_notes"])

# Rule 13: Use "" for clean URLs and status 201 for creation
@router.post("", response_model=VoiceNoteRead, status_code=status.HTTP_201_CREATED)
def create_voice_note(note: VoiceNoteCreate, db: Session = Depends(get_db)):
    try:
        return voice_note_service.create_voice_note(
            db=db,
            trade_id=note.trade_id,
            file_path=note.file_path,
            trade_state_at_time=note.trade_state_at_time,
        )
    except RuntimeError as e:
        # Rule 12: Explicit error handling
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trade/{trade_id}", response_model=List[VoiceNoteRead])
def list_voice_notes_for_trade(trade_id: int, db: Session = Depends(get_db)):
    return voice_note_service.list_voice_notes(db, trade_id)

@router.get("/{note_id}", response_model=VoiceNoteRead)
def get_voice_note(note_id: int, db: Session = Depends(get_db)):
    note = voice_note_service.get_voice_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Voice note not found")
    return note

@router.put("/{note_id}", response_model=VoiceNoteRead)
def update_voice_note(note_id: int, note_update: VoiceNoteUpdate, db: Session = Depends(get_db)):
    # Rule 7: Expect failure during update
    try:
        updated = voice_note_service.update_voice_note(
            db, 
            note_id, 
            file_path=note_update.file_path, 
            trade_state_at_time=note_update.trade_state_at_time
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Voice note not found")
        return updated
    except Exception:
        raise HTTPException(status_code=500, detail="Internal update error")

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voice_note(note_id: int, db: Session = Depends(get_db)):
    success = voice_note_service.delete_voice_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Voice note not found")
    # Rule 13: 204 No Content typically returns None/Empty
    return None 
