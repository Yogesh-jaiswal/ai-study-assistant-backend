from providers.base import Provider

from services.file_processors.embeddings.fake_embeddings import FakeEmbeddingGenerator

class FakeEmbeddingsProvider(Provider):
    def build(self, container):
        return FakeEmbeddingGenerator()