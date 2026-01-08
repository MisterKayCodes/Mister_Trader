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
    PORT: int = int(os.getenv("PORT", 5000))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database (Rule 2: Durable Storage)
    # FORCED TO SQLITE AS PER USER REQUEST
    DATABASE_URL: str = "sqlite:///./mister_trader.db"
    
    # Security (Rule 14: Phase 1 Authentication)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "7d3a5b2e1f4c6a8b9d0e1f2a3b4c5d6e")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 Day session
    
    # File Storage (Rule 2: Durable Storage - Phase 2)
    # Rule 11: Decoupling physical paths from business logic
    MEDIA_ROOT: str = "media"
    IMAGE_DIR: str = os.path.join(MEDIA_ROOT, "images")
    VOICE_DIR: str = os.path.join(MEDIA_ROOT, "voice")
    DOC_DIR: str = os.path.join(MEDIA_ROOT, "documents")
    
    # Integrations (Rule 11: Separate business logic from integrations)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

settings = Settings()
