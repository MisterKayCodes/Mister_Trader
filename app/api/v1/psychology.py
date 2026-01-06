from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.psychology import (
    TradePsychologyCreate,
    TradePsychologyRead,
    TradePsychologyUpdate,
)
from app.services import psychology_service

router = APIRouter(tags=["trade-psychology"])


@router.post("/", response_model=TradePsychologyRead)
def create_trade_psychology(
    payload: TradePsychologyCreate,
    db: Session = Depends(get_db),
):
    try:
        return psychology_service.create_trade_psychology(
            db=db,
            trade_id=payload.trade_id,
            discipline=payload.discipline,
            confidence=payload.confidence,
            followed_plan=payload.followed_plan,
            notes=payload.notes,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{psychology_id}", response_model=TradePsychologyRead)
def get_trade_psychology(
    psychology_id: int,
    db: Session = Depends(get_db),
):
    psychology = psychology_service.get_trade_psychology(db, psychology_id)
    if not psychology:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    return psychology


@router.get("/trade/{trade_id}", response_model=TradePsychologyRead)
def get_trade_psychology_by_trade(
    trade_id: int,
    db: Session = Depends(get_db),
):
    psychology = psychology_service.get_trade_psychology_by_trade(db, trade_id)
    if not psychology:
        raise HTTPException(status_code=404, detail="Trade psychology not found for trade")
    return psychology


@router.put("/{psychology_id}", response_model=TradePsychologyRead)
def update_trade_psychology(
    psychology_id: int,
    payload: TradePsychologyUpdate,
    db: Session = Depends(get_db),
):
    updated = psychology_service.update_trade_psychology(
        db=db,
        psychology_id=psychology_id,
        update=payload,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    return updated


@router.delete("/{psychology_id}")
def delete_trade_psychology(
    psychology_id: int,
    db: Session = Depends(get_db),
):
    success = psychology_service.delete_trade_psychology(db, psychology_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    return {"detail": "Trade psychology deleted successfully"}
