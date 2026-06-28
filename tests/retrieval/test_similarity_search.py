from services.retrieval.similarity_search_service import SimilaritySearchService

search_engine = SimilaritySearchService()

def test_retrieval(processed_file, logged_in_user):
    """
    Retrieving query related chunks
    """
    data = search_engine.search(
        processed_file["notebook_id"],
        logged_in_user["user_id"],
        "Paris is capital of France"
    )

    assert len(data) > 0

def test_multi_query_retrieval(processed_file, logged_in_user):
    """
    Retrieving multiple query related chunks
    """
    queries = [
        "What is Python?",
        "What framework is Flask?",
        "What is the capital of France?",
        "What stores information?",
        "What uses data?"
    ]

    for query in queries:
        data = search_engine.search(
            processed_file["notebook_id"],
            logged_in_user["user_id"],
            query
        )

        assert len(data) > 0

def test_other_user_retrieval(processed_file, second_logged_in_user):
    """
    Other should not retrieve someone else's notebook
    """
    data = search_engine.search(
        processed_file["notebook_id"],
        second_logged_in_user["user_id"],
        "Paris is capital of France"
    )

    assert len(data) == 0

def test_france_query_returns_france_chunk(
    processed_file,
    logged_in_user
):
    data = search_engine.search(
        processed_file["notebook_id"],
        logged_in_user["user_id"],
        "capital of france"
    )

    assert "France" in data[0][1]