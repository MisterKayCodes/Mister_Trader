from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.trade_media import TradeMediaRead
from app.api.v1.deps import get_current_user
from app.core.storage import save_upload_file

import app.services.media_service as media_service 

router = APIRouter(tags=["Trade Media"])

@router.post("/", response_model=TradeMediaRead, status_code=status.HTTP_201_CREATED)
def create_media(
    trade_id: int = Form(...),
    media_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        physical_path = save_upload_file(file, "images")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file to durable storage: {str(e)}"
        )

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
    return media_service.list_trade_media(
        db=db,
        user_id=current_user.id,
        trade_id=trade_id
    )

@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = media_service.delete_trade_media(
        db=db,
        user_id=current_user.id,
        media_id=media_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Media not found or unauthorized")
    return None
