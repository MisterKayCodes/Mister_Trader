from typing import Optional, Tuple, List


class TradeValidationError:
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
    
    def __str__(self):
        return f"{self.field}: {self.message}"


def validate_trade_entry(
    symbol: str,
    side: str,
    quantity: float,
    entry_price: Optional[float] = None,
    stop_loss: Optional[float] = None,
    take_profit: Optional[float] = None
) -> Tuple[bool, List[TradeValidationError]]:
    errors = []
    
    if not symbol or len(symbol) < 2:
        errors.append(TradeValidationError("symbol", "Symbol is required and must be at least 2 characters"))
    elif len(symbol) > 20:
        errors.append(TradeValidationError("symbol", "Symbol must be 20 characters or less"))
    
    valid_sides = ["BUY", "SELL", "LONG", "SHORT"]
    if not side or side.upper() not in valid_sides:
        errors.append(TradeValidationError("side", "Side must be BUY, SELL, LONG, or SHORT"))
    
    if quantity is None or quantity <= 0:
        errors.append(TradeValidationError("quantity", "Quantity must be greater than 0"))
    elif quantity > 1000000000:
        errors.append(TradeValidationError("quantity", "Quantity seems unreasonably large"))
    
    if entry_price is not None:
        if entry_price <= 0:
            errors.append(TradeValidationError("entry_price", "Entry price must be greater than 0"))
        elif entry_price > 1000000000:
            errors.append(TradeValidationError("entry_price", "Entry price seems unreasonably large"))
    
    if stop_loss is not None and entry_price is not None:
        if stop_loss <= 0:
            errors.append(TradeValidationError("stop_loss", "Stop loss must be greater than 0"))
        
        side_upper = side.upper() if side else ""
        if side_upper in ["BUY", "LONG"] and stop_loss >= entry_price:
            errors.append(TradeValidationError("stop_loss", "For a long trade, stop loss should be below entry price"))
        elif side_upper in ["SELL", "SHORT"] and stop_loss <= entry_price:
            errors.append(TradeValidationError("stop_loss", "For a short trade, stop loss should be above entry price"))
    
    if take_profit is not None and entry_price is not None:
        if take_profit <= 0:
            errors.append(TradeValidationError("take_profit", "Take profit must be greater than 0"))
        
        side_upper = side.upper() if side else ""
        if side_upper in ["BUY", "LONG"] and take_profit <= entry_price:
            errors.append(TradeValidationError("take_profit", "For a long trade, take profit should be above entry price"))
        elif side_upper in ["SELL", "SHORT"] and take_profit >= entry_price:
            errors.append(TradeValidationError("take_profit", "For a short trade, take profit should be below entry price"))
    
    return len(errors) == 0, errors


def calculate_risk_reward_ratio(
    side: str,
    entry_price: float,
    stop_loss: float,
    take_profit: float
) -> Optional[float]:
    if not all([entry_price, stop_loss, take_profit]):
        return None
    
    side_upper = side.upper()
    
    if side_upper in ["BUY", "LONG"]:
        risk = entry_price - stop_loss
        reward = take_profit - entry_price
    else:
        risk = stop_loss - entry_price
        reward = entry_price - take_profit
    
    if risk <= 0:
        return None
    
    return round(reward / risk, 2)


def format_validation_errors(errors: List[TradeValidationError]) -> str:
    if not errors:
        return "No errors"
    
    lines = ["Please fix the following issues:"]
    for error in errors:
        lines.append(f"- {error.message}")
    
    return "\n".join(lines)
