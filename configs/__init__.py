import os
from functools import cache

from .environments.base import BaseAppSettings
from .environments.development import get_development_overrides
from .environments.production import get_production_overrides
from .environments.testing import get_testing_overrides

@cache
def get_settings() -> BaseAppSettings:
    """Return the app settings based on the app enviroment"""
    
    base = BaseAppSettings()
    
    if base.ENVIRONMENT == "production":
        overrides =  get_production_overrides()
    
    elif base.ENVIRONMENT == "testing":
        overrides = get_testing_overrides()
    
    else:
        overrides = get_development_overrides()

    return base.model_copy(update=overrides)