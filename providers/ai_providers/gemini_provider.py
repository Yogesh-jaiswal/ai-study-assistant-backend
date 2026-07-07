from providers.base import Provider

from services.ai.models.gemini_provider import GeminiProvider

class GeminiAIProvider(Provider):
    def build(self, container):
        return GeminiProvider