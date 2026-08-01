from dataclasses import dataclass

from .retrieval_dataclasses import RetrievedChunk, ContextBundle

class ContextAssembler:

    @staticmethod
    def build_context(retrieved_chunks: list[RetrievedChunk]) -> ContextBundle:
        return ContextBundle(chunks=retrieved_chunks)