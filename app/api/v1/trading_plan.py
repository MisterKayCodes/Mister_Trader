from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.trading_plan_service import (
    create_trading_plan,
    get_trading_plan,
    get_todays_plan,
    list_trading_plans,
    update_trading_plan,
    delete_trading_plan
)

router = APIRouter(prefix="/plans", tags=["Trading Plans"])


class PlanCreate(BaseModel):
    title: str
    plan_date: Optional[date] = None
    market_bias: Optional[str] = None
    key_levels: Optional[str] = None
    watchlist: Optional[str] = None
    news_events: Optional[str] = None
    mental_state: Optional[str] = None
    max_trades: Optional[int] = None
    max_loss: Optional[str] = None
    notes: Optional[str] = None


class PlanUpdate(BaseModel):
    title: Optional[str] = None
    market_bias: Optional[str] = None
    key_levels: Optional[str] = None
    watchlist: Optional[str] = None
    news_events: Optional[str] = None
    mental_state: Optional[str] = None
    max_trades: Optional[int] = None
    max_loss: Optional[str] = None
    notes: Optional[str] = None


class PlanResponse(BaseModel):
    id: int
    title: str
    plan_date: Optional[date]
    market_bias: Optional[str]
    key_levels: Optional[str]
    watchlist: Optional[str]
    news_events: Optional[str]
    mental_state: Optional[str]
    max_trades: Optional[int]
    max_loss: Optional[str]
    notes: Optional[str]


@router.post("/", response_model=PlanResponse)
def create_new_plan(
    data: PlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = create_trading_plan(
        db,
        user_id=current_user.id,
        title=data.title,
        plan_date=data.plan_date,
        market_bias=data.market_bias,
        key_levels=data.key_levels,
        watchlist=data.watchlist,
        news_events=data.news_events,
        mental_state=data.mental_state,
        max_trades=data.max_trades,
        max_loss=data.max_loss,
        notes=data.notes
    )
    return plan


@router.get("/", response_model=List[PlanResponse])
def get_all_plans(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_trading_plans(db, current_user.id, limit)


@router.get("/today", response_model=Optional[PlanResponse])
def get_today_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = get_todays_plan(db, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="No plan for today")
    return plan


@router.get("/{plan_id}", response_model=PlanResponse)
def get_single_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = get_trading_plan(db, current_user.id, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
def update_existing_plan(
    plan_id: int,
    data: PlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = update_trading_plan(db, current_user.id, plan_id, **data.dict(exclude_none=True))
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.delete("/{plan_id}")
def delete_existing_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not delete_trading_plan(db, current_user.id, plan_id):
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}
