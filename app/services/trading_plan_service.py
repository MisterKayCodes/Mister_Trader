import logging
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from sqlalchemy.exc import SQLAlchemyError
from app.models.trading_plan import TradingPlan

logger = logging.getLogger(__name__)


def create_trading_plan(
    db: Session,
    user_id: int,
    title: str,
    plan_date: date = None,
    market_bias: str = None,
    key_levels: str = None,
    watchlist: str = None,
    news_events: str = None,
    mental_state: str = None,
    max_trades: int = None,
    max_loss: str = None,
    notes: str = None
) -> TradingPlan:
    try:
        plan = TradingPlan(
            user_id=user_id,
            title=title,
            plan_date=plan_date or date.today(),
            market_bias=market_bias,
            key_levels=key_levels,
            watchlist=watchlist,
            news_events=news_events,
            mental_state=mental_state,
            max_trades=max_trades,
            max_loss=max_loss,
            notes=notes
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create trading plan: {e}")
        raise RuntimeError("DATABASE_ERROR")


def get_trading_plan(db: Session, user_id: int, plan_id: int) -> Optional[TradingPlan]:
    stmt = select(TradingPlan).where(
        and_(TradingPlan.id == plan_id, TradingPlan.user_id == user_id)
    )
    return db.scalar(stmt)


def get_todays_plan(db: Session, user_id: int) -> Optional[TradingPlan]:
    stmt = select(TradingPlan).where(
        and_(TradingPlan.user_id == user_id, TradingPlan.plan_date == date.today())
    ).order_by(desc(TradingPlan.created_at))
    return db.scalar(stmt)


def list_trading_plans(db: Session, user_id: int, limit: int = 10) -> List[TradingPlan]:
    stmt = select(TradingPlan).where(TradingPlan.user_id == user_id).order_by(
        desc(TradingPlan.plan_date)
    ).limit(limit)
    return list(db.scalars(stmt).all())


def update_trading_plan(
    db: Session,
    user_id: int,
    plan_id: int,
    **kwargs
) -> Optional[TradingPlan]:
    plan = get_trading_plan(db, user_id, plan_id)
    if not plan:
        return None
    
    for key, value in kwargs.items():
        if hasattr(plan, key) and value is not None:
            setattr(plan, key, value)
    
    db.commit()
    db.refresh(plan)
    return plan


def delete_trading_plan(db: Session, user_id: int, plan_id: int) -> bool:
    plan = get_trading_plan(db, user_id, plan_id)
    if not plan:
        return False
    
    db.delete(plan)
    db.commit()
    return True


def format_plan_summary(plan: TradingPlan) -> str:
    lines = [f"<b>{plan.title}</b>"]
    lines.append(f"Date: {plan.plan_date}")
    
    if plan.market_bias:
        lines.append(f"\n<b>Bias:</b> {plan.market_bias}")
    
    if plan.watchlist:
        lines.append(f"\n<b>Watchlist:</b> {plan.watchlist}")
    
    if plan.key_levels:
        lines.append(f"\n<b>Key Levels:</b> {plan.key_levels}")
    
    if plan.mental_state:
        lines.append(f"\n<b>Mental State:</b> {plan.mental_state}")
    
    if plan.max_trades:
        lines.append(f"\n<b>Max Trades:</b> {plan.max_trades}")
    
    if plan.notes:
        lines.append(f"\n<b>Notes:</b> {plan.notes}")
    
    return "\n".join(lines)
