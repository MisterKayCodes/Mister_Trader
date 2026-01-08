from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """
    Rule 1: Stores the core identity and security state of a user.
    Rule 14: Never stores plain-text PINs; only the hashed version.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Using BigInteger for Telegram IDs is correct (Rule 13)
    telegram_user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    
    # Rule 14: The secret key for authentication
    hashed_pin = Column(String, nullable=False)
    
    # Rule 1: Tracking the state of the user account
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Rule 10: Observability for logs
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_user_id})>"
