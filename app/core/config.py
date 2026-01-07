import os
from dotenv import load_dotenv

# Rule 2: Load environment variables into the system state
load_dotenv()

class Settings:
    """
    Rule 1: Centralized configuration ensures the system is in a known state.
    Rule 13: Consistent naming and explicit defaults.
    """
    PROJECT_NAME: str = "Mister_Trader"
    
    # Server & Logging
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database (Rule 2: Durable Storage)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mister_trader.db")
    
    # Security (Rule 14: Phase 1 Authentication)
    # We removed API_KEY because we transitioned to JWT Tokens
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 Day session
    
    # Integrations (Rule 11: Separate business logic from integrations)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

settings = Settings()
