from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.voice_note import VoiceNoteRead, VoiceNoteUpdate 

# Rule 13: Standard 2026 Authentication imports
from app.api.v1.deps import get_current_user
from app.models.user import User

# Phase 2: Import our storage utilities
from app.core.storage import save_upload_file, delete_file

# FIX: Use 'import app.services.voice_note' to match your file name and avoid circular errors
import app.services.voice_note as voice_note_service 

router = APIRouter(tags=["voice-notes"])

@router.post("", response_model=VoiceNoteRead, status_code=status.HTTP_201_CREATED)
def create_voice_note(
    trade_id: int = Form(...),
    trade_state_at_time: str = Form(...),
    file: UploadFile = File(...), # The physical file stream
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Rule 14: Security Guard added
):
    """
    Rule 11: Decoupled logic. Route handles physical storage, service handles DB link.
    Rule 2: Durable Storage - Files are persisted to the 'voice' sub-directory.
    """
    # 1. Save the physical file to disk first
    try:
        physical_path = save_upload_file(file, "voice")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save voice file: {str(e)}")

    # 2. Save the resulting physical path and metadata to the database
    try:
        return voice_note_service.create_voice_note(
            db=db,
            user_id=current_user.id,
            trade_id=trade_id,
            file_path=physical_path, # Pass the real saved path
            trade_state_at_time=trade_state_at_time,
        )
    except RuntimeError as e:
        # Rule 2: If DB save fails, delete the physical file to prevent "ghost paths"
        delete_file(physical_path) 
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
    note_update: VoiceNoteUpdate, # Expects JSON for update fields
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    """Rule 1: Verify ownership before update."""
    try:
        updated = voice_note_service.update_voice_note(
            db=db, 
            note_id=note_id, 
            user_id=current_user.id,
            file_path=note_update.file_path, 
            trade_state_at_time=note_update.trade_state_at_time
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Voice note not found or unauthorized")
        return updated
    except Exception:
        raise HTTPException(status_code=500, detail="Internal update error")

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voice_note_route( # Renamed function slightly
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Rule 14: Security Guard added
):
    """Rule 2: Delete from DB AND disk."""
    # Get the note securely first to retrieve the file path
    note = voice_note_service.get_voice_note(db, note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Voice note not found or unauthorized")
        
    # Phase 2: Physically delete the file from the disk first
    if note.file_path:
        delete_file(note.file_path)

    # Then delete the database record
    success = voice_note_service.delete_voice_note(db, note_id, user_id=current_user.id)
    if not success:
        # If DB deletion somehow fails after file deletion, we log an error state
        raise HTTPException(status_code=500, detail="Failed to delete database record")
    return None
