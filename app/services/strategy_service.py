import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from app.models.strategy import Strategy

logger = logging.getLogger(__name__)


def create_strategy(
    db: Session,
    user_id: int,
    name: str,
    description: str = None,
    rules: str = None,
    entry_criteria: str = None,
    exit_criteria: str = None,
    risk_per_trade: str = None
) -> Strategy:
    try:
        strategy = Strategy(
            user_id=user_id,
            name=name,
            description=description,
            rules=rules,
            entry_criteria=entry_criteria,
            exit_criteria=exit_criteria,
            risk_per_trade=risk_per_trade
        )
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create strategy: {e}")
        raise RuntimeError("DATABASE_ERROR")


def get_strategy(db: Session, user_id: int, strategy_id: int) -> Optional[Strategy]:
    stmt = select(Strategy).where(
        and_(Strategy.id == strategy_id, Strategy.user_id == user_id)
    )
    return db.scalar(stmt)


def list_strategies(db: Session, user_id: int, active_only: bool = False) -> List[Strategy]:
    stmt = select(Strategy).where(Strategy.user_id == user_id)
    if active_only:
        stmt = stmt.where(Strategy.is_active == True)
    stmt = stmt.order_by(Strategy.name)
    return list(db.scalars(stmt).all())


def update_strategy(
    db: Session,
    user_id: int,
    strategy_id: int,
    **kwargs
) -> Optional[Strategy]:
    strategy = get_strategy(db, user_id, strategy_id)
    if not strategy:
        return None
    
    for key, value in kwargs.items():
        if hasattr(strategy, key) and value is not None:
            setattr(strategy, key, value)
    
    db.commit()
    db.refresh(strategy)
    return strategy


def delete_strategy(db: Session, user_id: int, strategy_id: int) -> bool:
    strategy = get_strategy(db, user_id, strategy_id)
    if not strategy:
        return False
    
    db.delete(strategy)
    db.commit()
    return True


def format_strategy_summary(strategy: Strategy) -> str:
    lines = [f"<b>{strategy.name}</b>"]
    
    if strategy.description:
        lines.append(f"\n{strategy.description}")
    
    if strategy.entry_criteria:
        lines.append(f"\n<b>Entry:</b> {strategy.entry_criteria}")
    
    if strategy.exit_criteria:
        lines.append(f"\n<b>Exit:</b> {strategy.exit_criteria}")
    
    if strategy.risk_per_trade:
        lines.append(f"\n<b>Risk:</b> {strategy.risk_per_trade}")
    
    return "\n".join(lines)
