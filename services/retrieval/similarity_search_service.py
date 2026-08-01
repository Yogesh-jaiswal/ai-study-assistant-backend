from repositories.embedding_repository import retrieve_similar_chunks
from services.file_processors.embeddings.embeddings_generator import EmbeddingGenerator
from configs import get_settings

from services.file_processors.document.doc_representation import DocumentBlock

from .top_k_search import top_k_search

from .retrieval_dataclasses import RetrievedChunk

class SimilaritySearchService:
    def __init__(self):
        self.embedder = EmbeddingGenerator()

    def search(self, notebook_id: str, user_id: str, query: str, k: int = 5) -> list[RetrievedChunk]:
        """
        Search query in stored embeddings and return top k result
        """
        query_embedding = self.embedder.embed(query)

        if get_settings().USE_PGVECTOR:
            result = retrieve_similar_chunks(notebook_id, user_id, query_embedding, k)
        else:
            result = top_k_search(notebook_id, user_id, query_embedding, k)

        return [
            RetrievedChunk(
                score=score,
                chunk=DocumentBlock(
                    type=chunk.block_type,
                    text=chunk.content,
                    metadata=chunk.chunk_metadata
                ),
                filename=upload.filename,
                author=upload.author,
                source_type=upload.source_type
            ) for (score, chunk, upload) in result
        ]
        

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