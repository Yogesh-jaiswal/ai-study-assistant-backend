from functools import lru_cache

from .environments.base import BaseAppSettings
from .environments.development import DevelopmentSettings
from .environments.production import ProductionSettings
from .environments.testing import TestingSettings

@lru_cache
def get_settings():
    env = BaseAppSettings().ENVIROMENT
    
    if env == "production":
        return ProductionSettings()
    
    elif env == "testing":
        return TestingSettings()
    
    return DevelopmentSettings()

settings = get_settings()