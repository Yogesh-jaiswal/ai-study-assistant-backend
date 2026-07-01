from typing import Any

def get_development_overrides() -> dict[str, Any]:
    """function to get the development environment config changes"""
    overrides = {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "AI_MODEL": "FAKE",
        "DATABASE_URL": "postgresql+psycopg://postgres:test%40@localhost:5432/ai_study_assistant",
        "USE_PGVECTOR": True,
        "LIMITER_STORAGE_URI": "memory://",
        "ACCESS_TOKEN_MINUTES": 15
    }

    return overrides