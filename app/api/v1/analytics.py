from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.analytics_service import (
    recalculate_user_stats,
    get_user_stats,
    get_win_rate,
    get_session_win_rates,
    get_strategy_performance,
    get_hourly_performance,
    get_day_of_week_performance,
    get_symbol_performance,
    get_psychology_insights
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stats = recalculate_user_stats(db, current_user.id)
    
    return {
        "total_trades": stats.total_trades,
        "winning_trades": stats.winning_trades,
        "losing_trades": stats.losing_trades,
        "breakeven_trades": stats.breakeven_trades,
        "win_rate": get_win_rate(stats),
        "total_pnl": stats.total_pnl,
        "best_trade_pnl": stats.best_trade_pnl,
        "worst_trade_pnl": stats.worst_trade_pnl,
        "current_streak": stats.current_streak,
        "current_streak_type": stats.current_streak_type,
        "best_win_streak": stats.best_win_streak,
        "worst_loss_streak": stats.worst_loss_streak,
        "avg_risk_reward": stats.avg_risk_reward
    }


@router.get("/sessions")
def get_session_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stats = get_user_stats(db, current_user.id)
    if not stats:
        return {"sessions": {}}
    
    session_rates = get_session_win_rates(stats)
    
    return {
        "sessions": session_rates,
        "details": {
            "london": {"wins": stats.london_wins, "losses": stats.london_losses},
            "newyork": {"wins": stats.newyork_wins, "losses": stats.newyork_losses},
            "asian": {"wins": stats.asian_wins, "losses": stats.asian_losses},
            "sydney": {"wins": stats.sydney_wins, "losses": stats.sydney_losses}
        }
    }


@router.get("/strategies")
def get_strategies_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    performance = get_strategy_performance(db, current_user.id)
    return {"strategies": performance}


@router.get("/hourly")
def get_hourly_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hourly = get_hourly_performance(db, current_user.id)
    return {"hourly": hourly}


@router.post("/refresh")
def refresh_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stats = recalculate_user_stats(db, current_user.id)
    return {"message": "Stats refreshed successfully", "total_trades": stats.total_trades}


@router.get("/days")
def get_day_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    days = get_day_of_week_performance(db, current_user.id)
    return {"days": days}


@router.get("/symbols")
def get_symbol_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    symbols = get_symbol_performance(db, current_user.id)
    return {"symbols": symbols}


@router.get("/psychology")
def get_psychology_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    psychology = get_psychology_insights(db, current_user.id)
    return psychology
