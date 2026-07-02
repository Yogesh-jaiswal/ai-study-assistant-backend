from sentence_transformers import SentenceTransformer

from configs import get_settings
from .base import BaseEmbeddingProvider

MODEL = SentenceTransformer(
    get_settings().EMBEDDINGS_MODEL
)

class EmbeddingGenerator(BaseEmbeddingProvider):

    def embed(self, text: str) -> list[float]:
        return MODEL.encode(text).tolist()
    
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return MODEL.encode(texts).tolist()