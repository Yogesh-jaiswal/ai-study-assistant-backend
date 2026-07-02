from .embeddings_generator import EmbeddingGenerator
from .fake_embeddings import FakeEmbeddingGenerator

class EmbeddingFactory:

    @staticmethod
    def get_provider(use_fake_emebedder: bool = False):
        return (
            FakeEmbeddingGenerator()
            if use_fake_emebedder
            else EmbeddingGenerator()
        )