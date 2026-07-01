from providers.base import Provider

from services.retrieval.top_k_search import top_k_search
from services.retrieval.similarity_search_service import SimilaritySearchService

class NumpyProvider(Provider):
    def build(self, container):
        return SimilaritySearchService(top_k_search)