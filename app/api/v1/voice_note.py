from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.voice_note import VoiceNoteCreate, VoiceNoteRead, VoiceNoteUpdate
from app.services import voice_note as voice_note_service

# Rule 13: Standard 2026 Authentication imports
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["voice_notes"])

@router.post("", response_model=VoiceNoteRead, status_code=status.HTTP_201_CREATED)
def create_voice_note(
    note: VoiceNoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Rule 14: Security Guard added
):
    """Rule 1: Create a note linked specifically to the logged-in user."""
    try:
        return voice_note_service.create_voice_note(
            db=db,
            user_id=current_user.id,  # Rule 1: Ensuring data ownership
            trade_id=note.trade_id,
            file_path=note.file_path,
            trade_state_at_time=note.trade_state_at_time,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trade/{trade_id}", response_model=List[VoiceNoteRead])
def list_voice_notes_for_trade(
    trade_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    """Rule 10: Only retrieve notes the current user is authorized to see."""
    return voice_note_service.list_voice_notes(db, trade_id, user_id=current_user.id)

@router.get("/{note_id}", response_model=VoiceNoteRead)
def get_voice_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    note = voice_note_service.get_voice_note(db, note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Voice note not found or unauthorized")
    return note

@router.put("/{note_id}", response_model=VoiceNoteRead)
def update_voice_note(
    note_id: int, 
    note_update: VoiceNoteUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    try:
        updated = voice_note_service.update_voice_note(
            db=db, 
            note_id=note_id, 
            user_id=current_user.id, # Rule 1: Verify ownership before update
            file_path=note_update.file_path, 
            trade_state_at_time=note_update.trade_state_at_time
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Voice note not found or unauthorized")
        return updated
    except Exception:
        raise HTTPException(status_code=500, detail="Internal update error")

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voice_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    success = voice_note_service.delete_voice_note(db, note_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Voice note not found or unauthorized")
    return None 
