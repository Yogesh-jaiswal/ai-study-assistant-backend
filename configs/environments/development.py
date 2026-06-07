from typing import Literal

from .base import BaseAppSettings

class DevelopmentSettings(BaseAppSettings):
    """Development settings object."""
    DEBUG: bool = True
    
    LOG_LEVEL: Literal["DEBUG"] = "DEBUG"

    AI_MODEL: Literal["FAKE"] = "FAKE"

    DATABASE_URL: str = "sqlite:///study_assistant.db"

    LIMITER_STORAGE_URI: str = "memory://"

    ACCESS_TOKEN_MINUTES: int = 15