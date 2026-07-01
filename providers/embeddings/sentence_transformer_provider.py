from providers.base import Provider

from services.embeddings.embeddings_generator import EmbeddingGenerator

class SentenceTransformerProvider(Provider):
    def build(self, container):
        return EmbeddingGenerator()