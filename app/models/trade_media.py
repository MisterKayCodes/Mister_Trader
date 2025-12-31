from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class TradeMedia(Base):
    __tablename__ = "trade_media"

    id = Column(Integer, primary_key=True, index=True)

    trade_id = Column(
        Integer,
        ForeignKey("trades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type = Column(String(50), nullable=False)  # e.g. ENTRY_SCREENSHOT, EXIT_SCREENSHOT

    file_path = Column(String, nullable=False)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
