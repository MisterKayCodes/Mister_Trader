from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.trade_media import TradeMediaCreate, TradeMediaRead
from app.api.v1.deps import get_current_user

# Rule 1: Use direct module import to break circular dependency
import app.services.media_service as media_service 

# Rule 13: Prefix is removed here because it is defined globally in main.py
# This prevents "Double Prefixing" (/api/v1/trade-media/trade-media/)
router = APIRouter(tags=["Trade Media"])

@router.post("/", response_model=TradeMediaRead, status_code=status.HTTP_201_CREATED)
def create_media(
    payload: TradeMediaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 11: Route extracts user_id from JWT and passes clean data to service.
    Rule 14: Data ownership is enforced by injecting current_user.id.
    """
    return media_service.create_trade_media(
        db=db,
        user_id=current_user.id,
        trade_id=payload.trade_id,
        media_type=payload.type,
        file_path=payload.file_path
    )

@router.get("/trade/{trade_id}", response_model=List[TradeMediaRead])
def list_media(
    trade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 14: List media for a specific trade strictly owned by the user.
    Uses Rule 6 (No Guessing) to ensure users only see their own records.
    """
    return media_service.list_trade_media(
        db=db,
        user_id=current_user.id,
        trade_id=trade_id
    )
