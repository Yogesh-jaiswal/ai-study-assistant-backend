from providers.base import Provider

from services.ai.models.fake_provider import FakeProvider

class FakeAIProvider(Provider):
    def build(self, container):
        return FakeProvider