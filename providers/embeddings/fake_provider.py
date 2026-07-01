from providers.base import Provider

from services.embeddings.fake_embeddings import FakeEmbeddingGenerator

class FakeEmbeddingsProvider(Provider):
    def build(self, container):
        return FakeEmbeddingGenerator()