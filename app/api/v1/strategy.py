from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.strategy_service import (
    create_strategy,
    get_strategy,
    list_strategies,
    update_strategy,
    delete_strategy
)

router = APIRouter(prefix="/strategies", tags=["Strategies"])


class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rules: Optional[str] = None
    entry_criteria: Optional[str] = None
    exit_criteria: Optional[str] = None
    risk_per_trade: Optional[str] = None


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[str] = None
    entry_criteria: Optional[str] = None
    exit_criteria: Optional[str] = None
    risk_per_trade: Optional[str] = None
    is_active: Optional[bool] = None


class StrategyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    rules: Optional[str]
    entry_criteria: Optional[str]
    exit_criteria: Optional[str]
    risk_per_trade: Optional[str]
    is_active: bool


@router.post("/", response_model=StrategyResponse)
def create_new_strategy(
    data: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = create_strategy(
        db,
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        rules=data.rules,
        entry_criteria=data.entry_criteria,
        exit_criteria=data.exit_criteria,
        risk_per_trade=data.risk_per_trade
    )
    return strategy


@router.get("/", response_model=List[StrategyResponse])
def get_all_strategies(
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_strategies(db, current_user.id, active_only)


@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_single_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = get_strategy(db, current_user.id, strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.put("/{strategy_id}", response_model=StrategyResponse)
def update_existing_strategy(
    strategy_id: int,
    data: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = update_strategy(db, current_user.id, strategy_id, **data.dict(exclude_none=True))
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.delete("/{strategy_id}")
def delete_existing_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not delete_strategy(db, current_user.id, strategy_id):
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"message": "Strategy deleted successfully"}
