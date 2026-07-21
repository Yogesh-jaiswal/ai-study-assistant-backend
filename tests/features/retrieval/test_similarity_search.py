import pytest
from services.retrieval.similarity_search_service import SimilaritySearchService

search_engine = SimilaritySearchService()

def test_retrieval(completed_upload, logged_in_user):
    """
    Retrieving query related chunks
    """
    data = search_engine.search(
        completed_upload["notebook_id"],
        logged_in_user["user_id"],
        "Paris is capital of France"
    )

    assert any("France" in chunk for _, chunk in data)

def test_multi_query_retrieval(completed_upload, logged_in_user):
    """
    Retrieving multiple query related chunks
    """
    queries = {
        "What is Python?": "Python",
        "What is the capital of France?": "Paris",
        "What stores structured information?": "SQL"
    }

    for query, expected in queries.items():
        data = search_engine.search(
            completed_upload["notebook_id"],
            logged_in_user["user_id"],
            query
        )

        assert any(expected in chunk for _, chunk in data)

def test_other_user_retrieval(completed_upload, second_logged_in_user):
    """
    Other should not retrieve someone else's notebook
    """
    data = search_engine.search(
        completed_upload["notebook_id"],
        second_logged_in_user["user_id"],
        "Paris is capital of France"
    )

    assert len(data) == 0

def test_france_query_returns_france_chunk(
    completed_upload,
    logged_in_user
):
    data = search_engine.search(
        completed_upload["notebook_id"],
        logged_in_user["user_id"],
        "capital of france"
    )

    assert "France" in data[0][1]