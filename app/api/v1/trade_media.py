from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
# Rule 13: Using the explicit names we defined in the schema file
from app.schemas.trade_media import TradeMediaCreate, TradeMediaRead
from app.services import media_service

router = APIRouter(
    # Rule 13: Standardized naming (matches your main.py registration)
    tags=["trade_media"]
)

@router.post(
    "", # Rule 13: Use empty string to avoid the double-slash // issue
    response_model=TradeMediaRead, # FIXED: Changed from MediaRead
    status_code=status.HTTP_201_CREATED
)
def create_media(
    media: TradeMediaCreate, # FIXED: Changed from MediaCreate
    db: Session = Depends(get_db)
):
    """
    Rule 1: Create a new media entry. Ensures system state is tracked.
    """
    try:
        return media_service.create_trade_media(
            db=db,
            trade_id=media.trade_id,
            media_type=media.type,
            file_path=media.file_path,
        )
    except RuntimeError as e:
        # Rule 12: Handle errors explicitly
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/trade/{trade_id}",
    # FIXED: Changed from MediaRead
    response_model=List[TradeMediaRead]
)
def list_media_for_trade(
    trade_id: int,
    db: Session = Depends(get_db)
):
    return media_service.list_trade_media(db, trade_id)

@router.get(
    "/{media_id}",
    # FIXED: Changed from MediaRead
    response_model=TradeMediaRead
)
def get_media(
    media_id: int,
    db: Session = Depends(get_db)
):
    media = media_service.get_trade_media(db, media_id)
    if not media:
        # Rule 1: Unknown entities return 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return media

@router.delete(
    "/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db)
):
    success = media_service.delete_trade_media(db, media_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return None # 204 No Content returns nothing
