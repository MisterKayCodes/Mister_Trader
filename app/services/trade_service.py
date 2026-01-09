from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate
from app.utils.session_utils import detect_trading_session


def create_trade(db: Session, user_id: int, trade_in: TradeCreate):
    trade_data = trade_in.model_dump()
    
    now_utc = datetime.now(timezone.utc)
    
    if not trade_data.get("open_timestamp"):
        trade_data["open_timestamp"] = now_utc
    
    if not trade_data.get("trading_session"):
        trade_data["trading_session"] = detect_trading_session(trade_data["open_timestamp"])
    
    if trade_data.get("day_of_week") is None:
        trade_data["day_of_week"] = trade_data["open_timestamp"].weekday()
    
    db_trade = Trade(**trade_data, user_id=user_id)
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def list_user_trades(db: Session, user_id: int, account_id: int):
    stmt = select(Trade).where(
        and_(Trade.user_id == user_id, Trade.account_id == account_id)
    )
    return db.execute(stmt).scalars().all()


def get_trade(db: Session, trade_id: int, user_id: int):
    stmt = select(Trade).where(
        and_(Trade.id == trade_id, Trade.user_id == user_id)
    )
    return db.execute(stmt).scalars().first()


def update_trade(db: Session, trade_id: int, user_id: int, trade_update: TradeUpdate):
    db_trade = get_trade(db, trade_id, user_id)
    if not db_trade:
        return None
    
    update_data = trade_update.model_dump(exclude_unset=True)
    
    if update_data.get("state") == "CLOSED" and update_data.get("exit_price"):
        if not update_data.get("close_timestamp"):
            update_data["close_timestamp"] = datetime.now(timezone.utc)
        
        if db_trade.entry_price and update_data.get("exit_price"):
            entry = db_trade.entry_price
            exit_price = update_data["exit_price"]
            side = db_trade.side
            qty = db_trade.quantity
            
            if side.upper() == "BUY":
                pnl = (exit_price - entry) * qty
            else:
                pnl = (entry - exit_price) * qty
            
            update_data["pnl"] = round(pnl, 2)
            
            if pnl > 0:
                update_data["outcome"] = "WIN"
            elif pnl < 0:
                update_data["outcome"] = "LOSS"
            else:
                update_data["outcome"] = "BREAKEVEN"
    
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


def calculate_risk_reward(entry_price: float, stop_loss: float, take_profit: float, side: str) -> float:
    if not all([entry_price, stop_loss, take_profit]):
        return None
    
    if side.upper() == "BUY":
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
    else:
        risk = abs(stop_loss - entry_price)
        reward = abs(entry_price - take_profit)
    
    if risk == 0:
        return None
    
    return round(reward / risk, 2)
