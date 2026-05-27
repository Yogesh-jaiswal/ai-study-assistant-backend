from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal, List

class Settings(BaseSettings):
    """Application settings object."""
    # App Settings
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")

    # Model Settings
    AI_MODEL: Literal["FAKE", "GEMINI"] = Field(default="FAKE")
    MODEL_API_KEY: str
    MODEL_NAME: str = Field(default="gemini-1.5-flash")

    # Quiz Settings
    DEFAULT_QUIZ_COUNT: int = Field(default = 5, ge = 1, le = 20)
    MAX_QUIZ_QUESTIONS: int = Field(default = 20, ge = 1)
    DEFAULT_QUIZ_LEVEL: Literal["easy", "medium", "hard"] = Field(default="medium")

    # Notes Settings
    MAX_NOTES_LENGTH: int = Field(default=1000)

    # Rate Limiter Settings
    RATELIMIT_ENABLED: bool = Field(default=True)
    DEFAULT_GLOBAL_LIMIT: List[str] = Field(default=["200/day", "50/hour"])
    LIMITER_STORAGE_URI: str = Field(default="memory://")
    LIMITER_STRATEGY: Literal["fixed-window", "moving-window", "sliding-window-counter"] = Field(default="fixed-window")
    RATELIMIT_HEADERS_ENABLED: bool = Field(default=True)
    SUMMARY_RATE_LIMIT: str = Field(default="10/minute")
    QUIZ_RATE_LIMIT: str = Field(default="5/minute")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()