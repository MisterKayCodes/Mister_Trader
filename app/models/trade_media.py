from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TradeMedia(Base):
    """
    Rule 1: Every media file must belong to a known user (Known State).
    Rule 14: Data ownership enforced at the database level.
    """
    __tablename__ = "trade_media"

    id = Column(Integer, primary_key=True, index=True)

    # Rule 14: The Security Link
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    trade_id = Column(
        Integer,
        ForeignKey("trades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type = Column(String(50), nullable=False)  # e.g. ENTRY_SCREENSHOT, EXIT_SCREENSHOT
    file_path = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Rule 13: Explicit relationships
    user = relationship("User", backref="media")
