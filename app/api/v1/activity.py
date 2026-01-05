from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.schemas.activity import ActivityCreate, ActivityRead
from app.services import activity_service

# Rule 13: Consistent prefixing in main.py, so we use "" here
router = APIRouter(tags=["activities"])

@router.post("", response_model=ActivityRead)
def log_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    try:
        return activity_service.log_activity(
            db=db,
            user_id=activity.user_id,
            activity_date=activity.date,
            activity_type=activity.activity_type
        )
    except ValueError as e:
        if str(e) == "MAX_ACTIVITY_LOGS_REACHED":
            raise HTTPException(status_code=400, detail="Daily limit reached")
        raise HTTPException(status_code=500, detail="Internal Logic Error")
    except Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")

@router.get("", response_model=List[ActivityRead])
def list_activities(user_id: int, activity_date: date = None, db: Session = Depends(get_db)):
    # Rule 6: Wait for explicit command (user_id is required by FastAPI here)
    return activity_service.list_activities(db, user_id, activity_date)

@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = activity_service.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    if not activity_service.delete_activity(db, activity_id):
        raise HTTPException(status_code=404, detail="Activity not found or delete failed")
    return {"detail": "Activity deleted successfully"}
