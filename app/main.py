from fastapi import FastAPI
import logging
import sys
from fastapi.responses import JSONResponse

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
