from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY_NAME = "Authorization"
API_KEY = os.getenv("API_KEY", "supersecretkey123")  # fallback key

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header
