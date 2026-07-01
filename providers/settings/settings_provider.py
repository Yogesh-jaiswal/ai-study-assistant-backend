from providers.base import Provider
from configs import get_settings


class SettingsProvider(Provider):

    def build(self, container):

        return get_settings()