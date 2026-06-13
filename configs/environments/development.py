from typing import Any

def get_development_overrides() -> dict[str, Any]:
    """function to get the development environment config changes"""
    overrides = {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "AI_MODEL": "FAKE",
        "DATABASE_URL": "sqlite:///study_assistant.db",
        "LIMITER_STORAGE_URI": "memory://",
        "ACCESS_TOKEN_MINUTES": 15
    }

    return overrides