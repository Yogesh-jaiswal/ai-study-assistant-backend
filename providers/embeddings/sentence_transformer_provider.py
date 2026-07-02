from providers.base import Provider

from services.file_processors.embeddings.embeddings_generator import EmbeddingGenerator

class SentenceTransformerProvider(Provider):
    def build(self, container):
        return EmbeddingGenerator()