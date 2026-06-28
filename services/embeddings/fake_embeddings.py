from .base import BaseEmbeddingProvider


class FakeEmbeddingGenerator(BaseEmbeddingProvider):

    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [
            [0.1, 0.2, 0.3]
            for _ in texts
        ]