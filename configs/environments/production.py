from typing import Literal

from .base import BaseAppSettings

class ProductionSettings(BaseAppSettings):
    """Production settings object."""
    DEBUG: bool = False

    LOG_LEVEL: Literal["INFO"] = "INFO"

    AI_MODEL: Literal["GEMINI"] = "GEMINI"

    RATELIMIT_ENABLED: bool = True

    # LIMITER_STORAGE_URI: str = "redis://..."

    ACCESS_TOKEN_MINUTES: int = 15