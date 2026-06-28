from typing import Any

def get_testing_overrides() -> dict[str, Any]:
    """function to get the testing environment config changes"""
    overrides = {
        "DEBUG": False,
        "LOG_LEVEL": "ERROR",
        "DATABASE_URL": "sqlite:///test.db",
        "USE_PGVECTOR": False,
        "RATELIMIT_ENABLED": False,
        "AI_MODEL": "FAKE",
        "CELERY_TASK_ALWAYS_EAGER": True,
        "CELERY_TASK_EAGER_PROPAGATES": True,
        "UPLOAD_FOLDER": "tests/tmp_uploads"
    }

    return overrides