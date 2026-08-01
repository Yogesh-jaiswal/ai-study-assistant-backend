from typing import Any

def get_testing_overrides() -> dict[str, Any]:
    """function to get the testing environment config changes"""
    overrides = {
        "DEBUG": False,
        "LOG_LEVEL": "ERROR",
        "POSTGRES_DB": "ai_study_assistant_test",
        "USE_PGVECTOR": False,
        "RATELIMIT_ENABLED": False,
        "AI_MODEL": "FAKE",
        "CELERY_TASK_ALWAYS_EAGER": True,
        "CELERY_TASK_EAGER_PROPAGATES": True,
        "UPLOAD_FOLDER": "tests/tmp_uploads"
    }

    return overrides