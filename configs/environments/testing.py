from typing import Literal

from .base import BaseAppSettings

class TestingSettings(BaseAppSettings):
    """Testing settings object."""
    DEBUG: bool = False

    LOG_LEVEL: Literal["ERROR"] = "ERROR"

    DATABASE_URL: str = "sqlite:///:memory:"

    RATELIMIT_ENABLED: bool = False

    AI_MODEL: Literal["FAKE"] = "FAKE"