from abc import ABC, abstractmethod

class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Returns the embeddings of the given chunk data"""
        pass

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Returns embeddings for multiple given chunks at once"""