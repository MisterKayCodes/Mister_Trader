from fastapi import FastAPI
import logging
import sys
from fastapi.responses import JSONResponse

# Import the users router
from app.api.v1 import users, accounts, trade_drafts, trades, activity

app = FastAPI()

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
    logger.info("Starting MisterTrader API server")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

# Add this line to include your routes
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(accounts.router, prefix="/api/v1/accounts")
app.include_router(trade_drafts.router, prefix="/api/v1/trade-drafts")
app.include_router(trades.router, prefix="/api/v1/trades")
app.include_router(activity.router, prefix="/api/v1/activities")
