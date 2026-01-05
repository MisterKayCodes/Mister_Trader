from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeRead, TradeUpdate

router = APIRouter(tags=["trades"])

@router.post("/", response_model=TradeRead)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    new_trade = Trade(**trade.dict(exclude_unset=True))
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

@router.get("/", response_model=List[TradeRead])
def list_trades(
    account_id: int = Query(..., description="Filter trades by account_id"),
    user_id: Optional[int] = Query(None, description="Optional filter by user_id"),
    db: Session = Depends(get_db),
):
    query = db.query(Trade).filter(Trade.account_id == account_id)
    if user_id is not None:
        query = query.filter(Trade.user_id == user_id)
    return query.all()

@router.get("/{trade_id}", response_model=TradeRead)
def get_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

@router.put("/{trade_id}", response_model=TradeRead)
def update_trade(trade_id: int, trade_update: TradeUpdate, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    update_data = trade_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trade, key, value)
    db.commit()
    db.refresh(trade)
    return trade

@router.delete("/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    db.delete(trade)
    db.commit()
    return {"detail": "Trade deleted"}
