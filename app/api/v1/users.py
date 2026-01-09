from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead, Token
from app.services import auth_service
from app.core.security import create_access_token
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["users"])

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = auth_service.get_user_by_telegram_id(db, user_in.telegram_user_id)
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")
    return auth_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, user_in.telegram_user_id, user_in.pin)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user.telegram_user_id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's info."""
    return current_user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
