import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, desc
from app.models.trade import Trade
from app.models.strategy import Strategy
from app.models.user_stats import UserStats
from app.utils.trade_utils import determine_trade_outcome, calculate_pnl
from app.utils.session_utils import detect_trading_session, get_session_display_name
from app.utils.streak_utils import calculate_streak, calculate_best_streaks

logger = logging.getLogger(__name__)


def get_user_stats(db: Session, user_id: int) -> Optional[UserStats]:
    stmt = select(UserStats).where(UserStats.user_id == user_id)
    return db.scalar(stmt)


def create_or_update_user_stats(db: Session, user_id: int) -> UserStats:
    stats = get_user_stats(db, user_id)
    if not stats:
        stats = UserStats(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


def recalculate_user_stats(db: Session, user_id: int) -> UserStats:
    stats = create_or_update_user_stats(db, user_id)
    
    trades_stmt = select(Trade).where(
        and_(Trade.user_id == user_id, Trade.state == "closed")
    ).order_by(Trade.close_timestamp)
    trades = db.scalars(trades_stmt).all()
    
    outcomes = []
    session_stats = {
        "LONDON": {"wins": 0, "losses": 0},
        "LONDON_NY": {"wins": 0, "losses": 0},
        "NEWYORK": {"wins": 0, "losses": 0},
        "ASIAN": {"wins": 0, "losses": 0},
        "SYDNEY": {"wins": 0, "losses": 0}
    }
    
    total_pnl = 0.0
    best_pnl = 0.0
    worst_pnl = 0.0
    rr_sum = 0.0
    rr_count = 0
    
    for trade in trades:
        outcome = trade.outcome or determine_trade_outcome(
            trade.side, trade.entry_price, trade.exit_price
        )
        outcomes.append(outcome)
        
        pnl = trade.pnl or calculate_pnl(
            trade.side, trade.entry_price, trade.exit_price, trade.quantity
        ) or 0.0
        total_pnl += pnl
        if pnl > best_pnl:
            best_pnl = pnl
        if pnl < worst_pnl:
            worst_pnl = pnl
        
        if trade.risk_reward_ratio:
            rr_sum += trade.risk_reward_ratio
            rr_count += 1
        
        session = trade.trading_session or detect_trading_session(trade.open_timestamp)
        if session and session in session_stats:
            if outcome == "WIN":
                session_stats[session]["wins"] += 1
            elif outcome == "LOSS":
                session_stats[session]["losses"] += 1
    
    wins = outcomes.count("WIN")
    losses = outcomes.count("LOSS")
    breakevens = outcomes.count("BREAKEVEN")
    
    current_streak, streak_type = calculate_streak(outcomes)
    best_win, worst_loss = calculate_best_streaks(outcomes)
    
    stats.total_trades = len(trades)
    stats.winning_trades = wins
    stats.losing_trades = losses
    stats.breakeven_trades = breakevens
    stats.total_pnl = round(total_pnl, 2)
    stats.best_trade_pnl = round(best_pnl, 2)
    stats.worst_trade_pnl = round(worst_pnl, 2)
    stats.current_streak = current_streak
    stats.current_streak_type = streak_type
    stats.best_win_streak = best_win
    stats.worst_loss_streak = worst_loss
    stats.avg_risk_reward = round(rr_sum / rr_count, 2) if rr_count > 0 else 0.0
    
    stats.london_wins = session_stats["LONDON"]["wins"] + session_stats["LONDON_NY"]["wins"]
    stats.london_losses = session_stats["LONDON"]["losses"] + session_stats["LONDON_NY"]["losses"]
    stats.newyork_wins = session_stats["NEWYORK"]["wins"] + session_stats["LONDON_NY"]["wins"]
    stats.newyork_losses = session_stats["NEWYORK"]["losses"] + session_stats["LONDON_NY"]["losses"]
    stats.asian_wins = session_stats["ASIAN"]["wins"]
    stats.asian_losses = session_stats["ASIAN"]["losses"]
    stats.sydney_wins = session_stats["SYDNEY"]["wins"]
    stats.sydney_losses = session_stats["SYDNEY"]["losses"]
    
    db.commit()
    db.refresh(stats)
    return stats


def get_win_rate(stats: UserStats) -> float:
    total = stats.winning_trades + stats.losing_trades
    if total == 0:
        return 0.0
    return round((stats.winning_trades / total) * 100, 1)


def get_session_win_rates(stats: UserStats) -> Dict[str, float]:
    result = {}
    
    for session, wins_attr, losses_attr in [
        ("London", "london_wins", "london_losses"),
        ("New York", "newyork_wins", "newyork_losses"),
        ("Asian", "asian_wins", "asian_losses"),
        ("Sydney", "sydney_wins", "sydney_losses")
    ]:
        wins = getattr(stats, wins_attr, 0)
        losses = getattr(stats, losses_attr, 0)
        total = wins + losses
        if total > 0:
            result[session] = round((wins / total) * 100, 1)
    
    return result


def get_strategy_performance(db: Session, user_id: int) -> List[Dict[str, Any]]:
    strategies_stmt = select(Strategy).where(Strategy.user_id == user_id)
    strategies = db.scalars(strategies_stmt).all()
    
    performance = []
    for strategy in strategies:
        trades_stmt = select(Trade).where(
            and_(Trade.user_id == user_id, Trade.strategy_id == strategy.id, Trade.state == "closed")
        )
        trades = db.scalars(trades_stmt).all()
        
        if not trades:
            continue
        
        wins = sum(1 for t in trades if t.outcome == "WIN")
        losses = sum(1 for t in trades if t.outcome == "LOSS")
        total = wins + losses
        
        total_pnl = sum(t.pnl or 0 for t in trades)
        
        performance.append({
            "id": strategy.id,
            "name": strategy.name,
            "trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": round((wins / total) * 100, 1) if total > 0 else 0,
            "total_pnl": round(total_pnl, 2)
        })
    
    return sorted(performance, key=lambda x: x["win_rate"], reverse=True)


def get_hourly_performance(db: Session, user_id: int) -> Dict[int, Dict[str, int]]:
    trades_stmt = select(Trade).where(
        and_(Trade.user_id == user_id, Trade.state == "closed")
    )
    trades = db.scalars(trades_stmt).all()
    
    hourly = {h: {"wins": 0, "losses": 0} for h in range(24)}
    
    for trade in trades:
        if trade.open_timestamp:
            hour = trade.open_timestamp.hour
            if trade.outcome == "WIN":
                hourly[hour]["wins"] += 1
            elif trade.outcome == "LOSS":
                hourly[hour]["losses"] += 1
    
    return hourly


def format_stats_overview(stats: UserStats) -> str:
    win_rate = get_win_rate(stats)
    
    lines = [
        f"Total Trades: {stats.total_trades}",
        f"Win Rate: {win_rate}%",
        f"Wins: {stats.winning_trades} | Losses: {stats.losing_trades} | BE: {stats.breakeven_trades}",
        f"",
        f"Total P&L: ${stats.total_pnl:,.2f}",
        f"Best Trade: ${stats.best_trade_pnl:,.2f}",
        f"Worst Trade: ${stats.worst_trade_pnl:,.2f}",
        f"",
        f"Current Streak: {stats.current_streak} {stats.current_streak_type or ''}".strip(),
        f"Best Win Streak: {stats.best_win_streak}",
        f"Worst Loss Streak: {stats.worst_loss_streak}",
    ]
    
    if stats.avg_risk_reward > 0:
        lines.append(f"Avg R:R: {stats.avg_risk_reward}")
    
    return "\n".join(lines)


def format_session_comparison(stats: UserStats) -> str:
    sessions = get_session_win_rates(stats)
    
    if not sessions:
        return "No session data available yet. Close some trades to see session performance."
    
    lines = ["Session Performance:"]
    for session, win_rate in sorted(sessions.items(), key=lambda x: x[1], reverse=True):
        wins_attr = f"{session.lower().replace(' ', '')}_wins"
        losses_attr = f"{session.lower().replace(' ', '')}_losses"
        
        wins = getattr(stats, wins_attr, 0) if hasattr(stats, wins_attr) else 0
        losses = getattr(stats, losses_attr, 0) if hasattr(stats, losses_attr) else 0
        
        lines.append(f"{session}: {win_rate}% ({wins}W / {losses}L)")
    
    return "\n".join(lines)
