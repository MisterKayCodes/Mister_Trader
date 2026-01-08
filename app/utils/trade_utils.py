"""
Trade Outcome Utilities

Determines if a trade is a WIN, LOSS, or BREAKEVEN based on:
- Trade side (BUY/Long or SELL/Short)
- Entry price vs Exit price
"""
from typing import Optional, Literal
from decimal import Decimal

TradeOutcome = Literal["WIN", "LOSS", "BREAKEVEN", "UNKNOWN"]

def determine_trade_outcome(
    side: str,
    entry_price: Optional[float],
    exit_price: Optional[float],
    tolerance: float = 0.0001
) -> TradeOutcome:
    """
    Determine trade outcome based on side and price comparison.
    
    BUY (Long) Trade:
        Win -> Exit Price > Entry Price
        Loss -> Exit Price < Entry Price
        Breakeven -> Exit Price = Entry Price
        
    SELL (Short) Trade:
        Win -> Exit Price < Entry Price
        Loss -> Exit Price > Entry Price  
        Breakeven -> Exit Price = Entry Price
    
    Args:
        side: Trade direction - "BUY", "LONG", "SELL", or "SHORT"
        entry_price: Entry/open price of the trade
        exit_price: Exit/close price of the trade
        tolerance: Price difference tolerance for breakeven (default 0.0001)
    
    Returns:
        TradeOutcome: "WIN", "LOSS", "BREAKEVEN", or "UNKNOWN" if prices missing
    """
    if entry_price is None or exit_price is None:
        return "UNKNOWN"
    
    entry = Decimal(str(entry_price))
    exit_p = Decimal(str(exit_price))
    diff = exit_p - entry
    tol = Decimal(str(tolerance))
    
    if abs(diff) <= tol:
        return "BREAKEVEN"
    
    side_upper = side.upper().strip()
    is_long = side_upper in ("BUY", "LONG")
    is_short = side_upper in ("SELL", "SHORT")
    
    if is_long:
        return "WIN" if diff > 0 else "LOSS"
    elif is_short:
        return "WIN" if diff < 0 else "LOSS"
    else:
        return "UNKNOWN"

def calculate_pnl(
    side: str,
    entry_price: Optional[float],
    exit_price: Optional[float],
    quantity: float = 1.0
) -> Optional[float]:
    """
    Calculate profit/loss for a trade.
    
    Args:
        side: Trade direction - "BUY", "LONG", "SELL", or "SHORT"
        entry_price: Entry/open price
        exit_price: Exit/close price
        quantity: Trade size/volume
    
    Returns:
        Float PnL value or None if prices missing
    """
    if entry_price is None or exit_price is None:
        return None
    
    side_upper = side.upper().strip()
    is_long = side_upper in ("BUY", "LONG")
    
    if is_long:
        pnl = (exit_price - entry_price) * quantity
    else:
        pnl = (entry_price - exit_price) * quantity
    
    return round(pnl, 4)

def calculate_pnl_percentage(
    side: str,
    entry_price: Optional[float],
    exit_price: Optional[float]
) -> Optional[float]:
    """
    Calculate percentage gain/loss for a trade.
    
    Returns:
        Float percentage (e.g., 5.5 for 5.5%) or None if prices missing
    """
    if entry_price is None or exit_price is None or entry_price == 0:
        return None
    
    side_upper = side.upper().strip()
    is_long = side_upper in ("BUY", "LONG")
    
    if is_long:
        pct = ((exit_price - entry_price) / entry_price) * 100
    else:
        pct = ((entry_price - exit_price) / entry_price) * 100
    
    return round(pct, 2)
