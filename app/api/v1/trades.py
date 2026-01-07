from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.trade import TradeCreate, TradeRead, TradeUpdate
from app.services import trade_service
# Rule 13 & 14: Standardized Auth Guard
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["trades"])

@router.post("", response_model=TradeRead, status_code=status.HTTP_201_CREATED)
def create_trade(
    trade: TradeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rule 1: New trades are strictly owned by the authenticated user."""
    return trade_service.create_trade(db=db, user_id=current_user.id, trade_in=trade)

@router.get("", response_model=List[TradeRead])
def list_trades(
    account_id: int = Query(..., description="Filter trades by account_id"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rule 14: Only return trades belonging to the authenticated owner."""
    return trade_service.list_user_trades(db=db, user_id=current_user.id, account_id=account_id)

@router.get("/{trade_id}", response_model=TradeRead)
def get_trade(
    trade_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trade = trade_service.get_trade(db=db, trade_id=trade_id, user_id=current_user.id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found or unauthorized")
    return trade

@router.put("/{trade_id}", response_model=TradeRead)
def update_trade(
    trade_id: int, 
    trade_update: TradeUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_trade = trade_service.update_trade(
        db=db, 
        trade_id=trade_id, 
        user_id=current_user.id, 
        trade_update=trade_update
    )
    if not updated_trade:
        raise HTTPException(status_code=404, detail="Trade not found or unauthorized")
    return updated_trade

@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trade(
    trade_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not trade_service.delete_trade(db=db, trade_id=trade_id, user_id=current_user.id):
        raise HTTPException(status_code=404, detail="Trade not found or unauthorized")
    return None
