from typing import Any

def get_production_overrides() -> dict[str, Any]:
    """function to get the production environment config changes"""
    overrides = {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "AI_MODEL": "GEMINI",
        "RATELIMIT_ENABLED": True,
        # "LIMITER_STORAGE_URI": "redis://...",
        "ACCESS_TOKEN_MINUTES": 15
    }

    return overrides