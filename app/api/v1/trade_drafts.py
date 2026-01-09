from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.trade_draft import TradeDraftCreate, TradeDraftRead, TradeDraftUpdate
from app.api.v1.deps import get_current_user
import app.services.draft_service as draft_service 

router = APIRouter(tags=["trade-drafts"])

@router.post("/", response_model=TradeDraftRead, status_code=status.HTTP_201_CREATED)
def create_trade_draft(
    payload: TradeDraftCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return draft_service.create_draft(db, user_id=current_user.id, draft_in=payload.model_dump())
    except ValueError:
        raise HTTPException(status_code=403, detail="Not authorized for this account")

@router.get("/", response_model=List[TradeDraftRead])
def list_trade_drafts(
    account_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Rule 14: strictly filter by account and owner."""
    return draft_service.list_drafts(db, user_id=current_user.id, account_id=account_id)

