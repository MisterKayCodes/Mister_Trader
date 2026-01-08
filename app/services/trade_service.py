from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate

# Rule 11: Business logic is separated from the API route
def create_trade(db: Session, user_id: int, trade_in: TradeCreate):
    # Rule 1: Always link the trade to the authenticated user
    db_trade = Trade(**trade_in.model_dump(), user_id=user_id)
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def list_user_trades(db: Session, user_id: int, account_id: int):
    # Rule 14: Security - only fetch trades where the user is the owner
    stmt = select(Trade).where(
        and_(Trade.user_id == user_id, Trade.account_id == account_id)
    )
    return db.execute(stmt).scalars().all()

def get_trade(db: Session, trade_id: int, user_id: int):
    # Rule 6: No guessing - find specific trade for specific user
    stmt = select(Trade).where(
        and_(Trade.id == trade_id, Trade.user_id == user_id)
    )
    return db.execute(stmt).scalars().first()

def update_trade(db: Session, trade_id: int, user_id: int, trade_update: TradeUpdate):
    db_trade = get_trade(db, trade_id, user_id)
    if not db_trade:
        return None
    
    # Rule 8: Boring, explicit update logic
    update_data = trade_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_trade, key, value)
    
    db.commit()
    db.refresh(db_trade)
    return db_trade

def delete_trade(db: Session, trade_id: int, user_id: int) -> bool:
    db_trade = get_trade(db, trade_id, user_id)
    if not db_trade:
        return False
    
    db.delete(db_trade)
    db.commit()
    return True
