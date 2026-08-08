from services.file_processors.embeddings.embeddings_generator import EmbeddingGenerator
from repositories.embedding_repository import get_embeddings_by_upload
from repositories.chunk_repository import get_chunks_by_upload

def test_embedding_generation():
    """Test that the EmbeddingGenerator can generate embeddings for a given text."""
    provider = EmbeddingGenerator()

    vector = provider.embed("Hello world")

    assert isinstance(vector, list)
    assert len(vector) > 0

def test_embedding_access(completed_upload, logged_in_user):
    """Test that embeddings can be accessed for a completed upload."""
    vectors = get_embeddings_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(vectors) > 0

def test_other_user_embedding_access(completed_upload, second_logged_in_user):
    """Test that another user cannot access embeddings for a completed upload."""
    vectors = get_embeddings_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        second_logged_in_user["user_id"]
    )

    assert len(vectors) == 0

def test_embedding_matches_chunk_count(completed_upload, logged_in_user):
    """Test that the number of embeddings matches the number of chunks for a completed upload."""
    chunks = get_chunks_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        logged_in_user["user_id"]
    )

    embeddings = get_embeddings_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(chunks) == len(embeddings)