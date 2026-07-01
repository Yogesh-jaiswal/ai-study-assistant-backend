from app.container.app_container import AppContainer

from providers.settings.settings_provider import SettingsProvider

from app.container.registries.embedding_registry import embedding_registry
from app.container.registries.provider_registry import retrieval_registry
# from app.container.registries.ai_registry import ai_registry


class CompositionRoot:

    def __init__(self):

        self.container = AppContainer()

        self.settings_provider = SettingsProvider()

    def compose(self):

        self._build_settings()

        self._build_embeddings()

        self._build_retrieval()

        self._build_ai()

        return self.container