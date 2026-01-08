from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.services import auth_service

# Rule 13: Standard 2026 way to find the "Badge" in the request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    The 'Security Guard'. 
    Rule 1: Ensures the system knows EXACTLY who is making the request.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Rule 14: Decrypt the badge using our secret vault key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telegram_user_id: str = payload.get("sub")
        if telegram_user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Rule 6: No guessing - find the user in Durable Storage (Rule 2)
    user = auth_service.get_user_by_telegram_id(db, telegram_id=int(telegram_user_id))
    if user is None:
        raise credentials_exception
    return user
