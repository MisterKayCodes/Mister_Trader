from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.trade_draft import TradeDraft
from app.schemas.trade_draft import TradeDraftCreate, TradeDraftRead

router = APIRouter(tags=["trade-drafts"])


@router.post("/", response_model=TradeDraftRead)
def create_trade_draft(draft: TradeDraftCreate, db: Session = Depends(get_db)):
    new_draft = TradeDraft(**draft.dict())
    db.add(new_draft)
    db.commit()
    db.refresh(new_draft)
    return new_draft


@router.get("/", response_model=List[TradeDraftRead])
def list_trade_drafts(account_id: int, db: Session = Depends(get_db)):
    return db.query(TradeDraft).filter(
        TradeDraft.account_id == account_id
    ).all()


@router.get("/{draft_id}", response_model=TradeDraftRead)
def get_trade_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.query(TradeDraft).filter(TradeDraft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Trade draft not found")
    return draft


@router.delete("/{draft_id}")
def delete_trade_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.query(TradeDraft).filter(TradeDraft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Trade draft not found")

    db.delete(draft)
    db.commit()
    return {"detail": "Trade draft deleted"}
