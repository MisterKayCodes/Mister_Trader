from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

# Rule 11: Import logic/dependencies from their respective modules
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.schemas.activity import ActivityCreate, ActivityRead

# Rule 1: Use direct import to avoid circular dependency crashes
import app.services.activity_service as activity_service

router = APIRouter(tags=["activities"])

@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def log_activity(
    activity: ActivityCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Rule 14: Security Guard identifies user
):
    """
    Rule 11: Route strictly handles request/response and passes verified user_id 
    to the service layer.
    """
    return activity_service.log_activity(
        db=db,
        user_id=current_user.id,
        activity_date=activity.date,
        activity_type=activity.activity_type
    )

@router.get("", response_model=List[ActivityRead])
def list_activities(
    activity_date: date = None, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 14: Ownership enforced. Only returns activities belonging 
    to the authenticated user.
    """
    return activity_service.list_activities(
        db=db, 
        user_id=current_user.id, 
        activity_date=activity_date
    )

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Rule 6: No guessing. Ensures the user owns the activity 
    before allowing deletion.
    """
    success = activity_service.delete_activity_secure(
        db=db, 
        activity_id=activity_id, 
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found or unauthorized")
    return None
