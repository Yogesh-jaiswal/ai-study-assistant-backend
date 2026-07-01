from providers.base import Provider

from repositories.embedding_repository import search_top_k_chunks
from services.retrieval.similarity_search_service import SimilaritySearchService

class PGVectorProvider(Provider):
    def build(self, container):
        return SimilaritySearchService(search_top_k_chunks)