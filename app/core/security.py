from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings 

# Rule 14: Using the industry-standard bcrypt for 2026
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pin(pin: str) -> str:
    safe_pin = str(pin)[:72]
    return pwd_context.hash(safe_pin)

def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Checks if a PIN matches the scrambled hash."""
    return pwd_context.verify(plain_pin, hashed_pin)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Rule 1: Creates a verifiable session badge (JWT)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
