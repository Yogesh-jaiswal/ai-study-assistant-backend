from typing import Any

def get_testing_overrides() -> dict[str, Any]:
    """function to get the testing environment config changes"""
    overrides = {
        "DEBUG": False,
        "LOG_LEVEL": "ERROR",
        "DATABASE_URL": "sqlite://",
        "RATELIMIT_ENABLED": False,
        "AI_MODEL": "FAKE"
    }

    return overrides