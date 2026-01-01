from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(
    tags=["users"]
)

# Test route to verify router is working
@router.get("/test")
async def test_route():
    return {"message": "Users router is working"}

# Create a new user
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with this telegram_user_id already exists
    existing_user = db.query(User).filter(User.telegram_user_id == user.telegram_user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Telegram user already registered")
    
    new_user = User(telegram_user_id=user.telegram_user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get user by ID
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
