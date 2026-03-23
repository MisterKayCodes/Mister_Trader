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
    
    # Auto-detect state if exit_price is provided
    if update_data.get("exit_price") is not None and update_data.get("state") not in ["closed", "CLOSED"]:
        update_data["state"] = "closed"

    current_entry = update_data.get("entry_price", db_trade.entry_price)
    
    if (update_data.get("state") == "closed" or update_data.get("state") == "CLOSED") and update_data.get("exit_price") is not None:
        if not update_data.get("close_timestamp") and not db_trade.close_timestamp:
            update_data["close_timestamp"] = datetime.now(timezone.utc)
        
        if current_entry is not None:
            entry_price = float(current_entry)
            exit_price = float(update_data["exit_price"])
            side = update_data.get("side", db_trade.side)
            qty = update_data.get("quantity", db_trade.quantity)
            
            pnl = (exit_price - entry_price) * qty if side.upper() in ["BUY", "LONG"] else (entry_price - exit_price) * qty
            
            update_data["pnl"] = round(pnl, 2)
            
            if pnl > 0:
                update_data["outcome"] = "WIN"
            elif pnl < 0:
                update_data["outcome"] = "LOSS"
            else:
                update_data["outcome"] = "BREAK_EVEN"
    
    for key, value in update_data.items():
        setattr(db_trade, key, value)
    
    db.commit()
    db.refresh(db_trade)
    # Automatically recalculate statistics when a trade is closed
    if db_trade.state == "closed":
        from app.services.analytics_service import recalculate_user_stats
        recalculate_user_stats(db, user_id)
    return db_trade


def delete_trade(db: Session, trade_id: int, user_id: int) -> bool:
    db_trade = get_trade(db, trade_id, user_id)
    if not db_trade:
        return False
    
    # Rule 2: Physical storage cleanup before DB deletion
    from app.core.storage import delete_file
    
    # 1. Cleanup associated Trade Media (screenshots)
    if hasattr(db_trade, 'media') and db_trade.media:
        for media in db_trade.media:
            if media.file_path:
                delete_file(media.file_path)
                
    # 2. Cleanup associated Voice Notes
    if hasattr(db_trade, 'voice_notes') and db_trade.voice_notes:
        for voice in db_trade.voice_notes:
            if voice.file_path:
                delete_file(voice.file_path)

    db.delete(db_trade)
    db.commit()

    # Rule 8: Ensure stats are fresh after record removal
    try:
        from app.services.analytics_service import recalculate_user_stats
        recalculate_user_stats(db, user_id)
    except Exception:
        pass # Non-critical if stats fail to recalc
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
