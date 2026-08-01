from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class TokenEncoding:
    offset_mapping: list[tuple[int, int]]

class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the total number of tokens in the given text block."""
        pass

    @abstractmethod
    def offset_mapping(self, text: str) -> TokenEncoding:
        """Return the offset mapping of the using the tokenizer associated with this embedding model."""

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Maximum supported input tokens for this embedding model."""