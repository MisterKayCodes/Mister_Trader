from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead, Token
from app.services import auth_service # Rule 11: Logic lives in services
from app.core.security import create_access_token

router = APIRouter(tags=["users"])

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # Rule 5: Idempotency check before creating
    existing = auth_service.get_user_by_telegram_id(db, user_in.telegram_user_id)
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")
    return auth_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    # Rule 6: No guessing - check credentials explicitly
    user = auth_service.authenticate_user(db, user_in.telegram_user_id, user_in.pin)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Rule 1: Known state - generate a verifiable session badge
    token = create_access_token(data={"sub": str(user.telegram_user_id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
