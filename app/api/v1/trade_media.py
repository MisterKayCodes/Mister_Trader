from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.trade_media import TradeMediaRead
from app.api.v1.deps import get_current_user
from app.core.storage import save_upload_file  # Phase 2 Storage Utility

# Rule 1: Use direct module import to break circular dependency
import app.services.media_service as media_service 

# Rule 13: Prefix is managed in main.py to prevent double-prefixing
router = APIRouter(tags=["Trade Media"])

@router.post("/", response_model=TradeMediaRead, status_code=status.HTTP_201_CREATED)
def create_media(
    trade_id: int = Form(...),
    media_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 11: Business logic for physical storage is decoupled from database linking.
    Rule 2: Durable Storage - Files are physically persisted to the 'images' sub-directory.
    Rule 14: Data ownership is enforced by passing current_user.id to the service.
    """
    
    # 1. Save the physical file to disk first
    try:
        # We specify "images" to match your media/images directory structure
        physical_path = save_upload_file(file, "images")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file to durable storage: {str(e)}"
        )

    # 2. Pass the resulting physical path and metadata to the service layer
    return media_service.create_trade_media(
        db=db,
        user_id=current_user.id,
        trade_id=trade_id,
        media_type=media_type,
        file_path=physical_path
    )

@router.get("/trade/{trade_id}", response_model=List[TradeMediaRead])
def list_media(
    trade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 14: Ownership check. Only lists media for trades owned by the authenticated user.
    """
    return media_service.list_trade_media(
        db=db,
        user_id=current_user.id,
        trade_id=trade_id
    )
