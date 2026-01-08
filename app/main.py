import os
import logging
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
# Import the routers
from app.api.v1 import (
    users, accounts, trade_drafts, trades, 
    activity, trade_media, psychology, voice_note,
    analytics, strategy, trading_plan, export
)

app = FastAPI(title=settings.PROJECT_NAME)

# Setup structured JSON logging
logger = logging.getLogger("mistertrader")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.on_event("startup")
async def startup_event():
    """
    Rule 1: Ensure the system starts in a known state.
    Rule 2: Prepare durable storage directories on boot.
    """
    logger.info("Starting MisterTrader API server")
    
    # Initialize Phase 2 Storage Folders
    directories = [settings.IMAGE_DIR, settings.VOICE_DIR, settings.DOC_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created storage directory: {directory}")

# Rule 17: Serve static files so you can actually view your images/voice notes
# This makes the 'media' folder accessible via URL (e.g., /media/images/photo.jpg)
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

@app.get("/")
async def root():
    return {"message": "MisterTrader API is running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

# Include Routers
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(accounts.router, prefix="/api/v1/accounts")
app.include_router(trade_drafts.router, prefix="/api/v1/trade-drafts")
app.include_router(trades.router, prefix="/api/v1/trades")
app.include_router(activity.router, prefix="/api/v1/activities")
app.include_router(trade_media.router, prefix="/api/v1/trade-media")
app.include_router(psychology.router, prefix="/api/v1/trade-psychology")
app.include_router(voice_note.router, prefix="/api/v1/voice-notes")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(strategy.router, prefix="/api/v1")
app.include_router(trading_plan.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
