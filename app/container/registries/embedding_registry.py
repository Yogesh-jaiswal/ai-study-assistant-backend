from .base_registry import Registory

from providers.embeddings.fake_provider import FakeEmbeddingsProvider
from providers.embeddings.sentence_transformer_provider import SentenceTransformerProvider

EMBEDDING_PROVIDERS = {
    "fake": FakeEmbeddingsProvider,
    "sentence-transformer": SentenceTransformerProvider
}

embedding_registry = Registory(EMBEDDING_PROVIDERS)