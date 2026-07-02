from repositories.embedding_repository import search_top_k_chunks
from services.file_processors.embeddings.embeddings_generator import EmbeddingGenerator
from configs import get_settings

from .top_k_search import top_k_search

class SimilaritySearchService:

    def search(self, notebook_id: str, user_id: str, query: str, k: int = 5) -> list[tuple[float, str]]:
        """
        Search query in stored embeddings and return top k result
        """
        embedder = EmbeddingGenerator()

        query_embeddings = embedder.embed(query)

        if get_settings().USE_PGVECTOR:
            return search_top_k_chunks(notebook_id, user_id, query_embeddings, k)
        else:
            return top_k_search(notebook_id, user_id, query_embeddings, k)
        

"""
from services.embeddings.embeddings_generator import EmbeddingGenerator
from collections.abc import Callable
from typing import Any

class SimilaritySearchService:
    def __init__(self, search_func: Callable[..., Any]):
        self._search_func = search_func


    def search(self, notebook_id: str, user_id: str, query: str, k: int = 5) -> list[tuple[float, str]]:
        '''
        Search query in stored embeddings and return top k result
        '''
        embedder = EmbeddingGenerator()

        query_embeddings = embedder.embed(query)

        self._search_func(notebook_id, user_id, query_embeddings, k)
"""