# app/api/v1/psychology.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.psychology import (
    TradePsychologyCreate,
    TradePsychologyRead,
    TradePsychologyUpdate,
)
# Use direct import to avoid circular dependency
import app.services.psychology_service as psychology_service 
from app.api.v1.deps import get_current_user # Import the security guard

router = APIRouter(tags=["trade-psychology"])


@router.post("/", response_model=TradePsychologyRead, status_code=status.HTTP_201_CREATED)
def create_trade_psychology(
    payload: TradePsychologyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), # <-- Added Guard
):
    """Rule 14: Use user_id from token to verify trade ownership."""
    try:
        return psychology_service.create_trade_psychology(
            db=db,
            user_id=current_user.id, # <-- Pass the ID
            trade_id=payload.trade_id,
            discipline=payload.discipline,
            confidence=payload.confidence,
            followed_plan=payload.followed_plan,
            decision_quality=payload.decision_quality,
            emotions=payload.emotions,
            market_condition=payload.market_condition,
            volatility_level=payload.volatility_level,
            notes=payload.notes,
        )
    except ValueError as e:
        # Catch our specific unauthorized error
         raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{psychology_id}", response_model=TradePsychologyRead)
def get_trade_psychology(
    psychology_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), # <-- Added Guard
):
    """Rule 14: Only fetch psychology if the user owns the parent trade."""
    psychology = psychology_service.get_trade_psychology(db, current_user.id, psychology_id)
    if not psychology:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    return psychology


@router.get("/trade/{trade_id}", response_model=TradePsychologyRead)
def get_trade_psychology_by_trade(
    trade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), # <-- Added Guard
):
    """Rule 14: Only fetch psychology by trade ID if user owns that trade."""
    psychology = psychology_service.get_trade_psychology_by_trade(db, current_user.id, trade_id)
    if not psychology:
        # It's better not to confirm the trade exists if they don't own it
        raise HTTPException(status_code=404, detail="Trade psychology not found") 
    return psychology


@router.put("/{psychology_id}", response_model=TradePsychologyRead)
def update_trade_psychology(
    psychology_id: int,
    payload: TradePsychologyUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), # <-- Added Guard
):
    """Rule 14: Verify ownership before updating psychology record."""
    updated = psychology_service.update_trade_psychology(
        db=db,
        user_id=current_user.id, # <-- Pass the ID
        psychology_id=psychology_id,
        update=payload,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    return updated


@router.delete("/{psychology_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trade_psychology(
    psychology_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), # <-- Added Guard
):
    """Rule 14: Verify ownership before deletion."""
    success = psychology_service.delete_trade_psychology(db, current_user.id, psychology_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trade psychology not found")
    # Return 204 No Content, no JSON body required for successful delete
    return None
