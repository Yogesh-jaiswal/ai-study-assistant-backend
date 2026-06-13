from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from typing import Literal, List
from pathlib import Path

class BaseAppSettings(BaseSettings):
    """Application settings object."""
    # App Settings
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="DEBUG")
    ENVIRONMENT: Literal["development", "testing", "production"] = Field(default="development")

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

    # Database Settings
    DATABASE_URL: str = Field(default="sqlite:///study_assistant.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(default=False)

    # Upload Settings
    MAX_CONTENT_LENGTH: int = Field(default=500000)

    # JWT Settings
    JWT_PRIVATE_KEY_PATH: Path = Field(default="keys/private.pem")
    JWT_PUBLIC_KEY_PATH: Path = Field(default="keys/public.pem")
    JWT_ALGORITHM: str = Field(default="RS256")
    ACCESS_TOKEN_MINUTES: int = Field(default=15)

    @computed_field
    @property
    def jwt_private_key(self) -> str:
        return self.JWT_PRIVATE_KEY_PATH.read_text()

    @computed_field
    @property
    def jwt_public_key(self) -> str:
        return self.JWT_PUBLIC_KEY_PATH.read_text()
    
    # Login Settings
    DUMMY_HASH: str

    # Redis Settings
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )