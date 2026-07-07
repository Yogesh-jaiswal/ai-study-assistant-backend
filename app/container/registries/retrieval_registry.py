from .base_registry import Registory

from providers.retrieval.numpy_provider import NumpyProvider
from providers.retrieval.pg_vector_provider import PGVectorProvider

RETRIEVAL_PROVIDERS = {
    "numpy": NumpyProvider,
    "pg-vector": PGVectorProvider
}

retrievl_registry = Registory(RETRIEVAL_PROVIDERS)