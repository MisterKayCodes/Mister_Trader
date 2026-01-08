import csv
import io
import logging
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.trade import Trade
from app.models.strategy import Strategy

logger = logging.getLogger(__name__)


def export_trades_to_csv(db: Session, user_id: int) -> io.BytesIO:
    stmt = select(Trade).where(Trade.user_id == user_id).order_by(Trade.created_at.desc())
    trades = db.scalars(stmt).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    headers = [
        "ID", "Symbol", "Side", "Quantity",
        "Entry Price", "Exit Price", "Stop Loss", "Take Profit",
        "P&L", "R:R Ratio", "Outcome", "State",
        "Strategy", "Session", "Notes",
        "Open Time", "Close Time", "Created At"
    ]
    writer.writerow(headers)
    
    strategy_cache = {}
    
    for trade in trades:
        strategy_name = ""
        if trade.strategy_id:
            if trade.strategy_id not in strategy_cache:
                strat = db.scalar(select(Strategy).where(Strategy.id == trade.strategy_id))
                strategy_cache[trade.strategy_id] = strat.name if strat else ""
            strategy_name = strategy_cache[trade.strategy_id]
        
        row = [
            trade.id,
            trade.symbol,
            trade.side,
            trade.quantity,
            trade.entry_price or "",
            trade.exit_price or "",
            trade.stop_loss or "",
            trade.take_profit or "",
            trade.pnl or "",
            trade.risk_reward_ratio or "",
            trade.outcome or "",
            trade.state,
            strategy_name,
            trade.trading_session or "",
            trade.notes or "",
            trade.open_timestamp.isoformat() if trade.open_timestamp else "",
            trade.close_timestamp.isoformat() if trade.close_timestamp else "",
            trade.created_at.isoformat() if trade.created_at else ""
        ]
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    bytes_io = io.BytesIO()
    bytes_io.write(csv_content.encode('utf-8'))
    bytes_io.seek(0)
    
    return bytes_io


def get_export_filename(user_id: int) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"trades_export_{user_id}_{timestamp}.csv"
