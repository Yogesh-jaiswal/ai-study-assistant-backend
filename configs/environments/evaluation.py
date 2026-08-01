from typing import Any

def get_evaluation_overrides() -> dict[str, Any]:
    """function to get the evaluation environment config changes"""
    overrides = {
        "CELERY_TASK_ALWAYS_EAGER": True,
        "CELERY_TASK_EAGER_PROPAGATES": True,
        "LOG_LEVEL": "WARNING"
    }

    return overrides