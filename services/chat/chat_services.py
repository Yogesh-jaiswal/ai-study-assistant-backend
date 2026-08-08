from dataclasses import asdict

from services.retrieval.similarity_search_service import SimilaritySearchService
from services.retrieval.context_assembler import ContextAssembler
from services.retrieval.citation_builder import CitationBuilder

from .chat_generator import ChatGenerator

from validators.query_schemas import QueryRequest

def answer_query(notebook_id: str, user_id: str, payload: QueryRequest) -> dict[str, str]:
    """Generates the response for the asked query."""
    search_engine = SimilaritySearchService()

    search_response = search_engine.search(notebook_id, user_id, payload.question)

    if not search_response:
        return {
            "response": "Sorry, I couldn't find the information in your notes."
        }

    context = ContextAssembler.build_context(search_response)

    generator = ChatGenerator()

    response = generator.generate(
        question=payload.question, 
        context=context.to_text()
    )

    citations = CitationBuilder.build(search_response)

    return {
        "citations": [asdict(c) for c in citations],
        **response
    }