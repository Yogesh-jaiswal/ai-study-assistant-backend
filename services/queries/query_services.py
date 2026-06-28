from services.retrieval.similarity_search_service import SimilaritySearchService
from services.ai.llm_client import generate_response
from services.ai.context_assembler import ContextAssembler

from validators.query_schemas import QueryRequest, QueryServiceRequest

def answer_query(notebook_id: str, user_id: str, payload: QueryRequest) -> dict[str, str]:
    """Generates the response for the asked query"""
    search_engine = SimilaritySearchService()

    search_response = search_engine.search(notebook_id, user_id, payload.question)

    if not search_response:
        return {
            "response":
            "Sorry, I couldn't find the information in your notes."
        }

    context = ContextAssembler.build_context(
        [content for _, content in search_response]
    )

    response = generate_response(QueryServiceRequest(
        question=payload.question,
        context=context
    ), "ask")

    return response