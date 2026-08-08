"""
Configuration package for the AI Study Assistant backend.

Provides shared configuration values and environment-specific
application configuration used across development, testing,
evaluation, and production environments.
"""

from functools import cache

from .environments.base import BaseAppSettings
from .environments.production import get_production_overrides
from .environments.testing import get_testing_overrides
from .environments.evaluation import get_evaluation_overrides

@cache
def get_settings() -> BaseAppSettings:
    """Return the app settings based on the app enviroment"""

    settings_overrides = {
        "production": get_production_overrides,
        "testing": get_testing_overrides,
        "evaluation": get_evaluation_overrides
    }

    base = BaseAppSettings()

    overrides_func = settings_overrides.get(base.ENVIRONMENT)
    if overrides_func:
        overrides = overrides_func()
    else:
        overrides = {}

    return base.model_copy(update=overrides)