from services.embeddings.embeddings_generator import EmbeddingGenerator
from repositories.embedding_repository import get_embeddings_by_upload
from repositories.chunk_repository import get_chunks_by_upload

def test_embedding_generation():
    provider = EmbeddingGenerator()

    vector = provider.embed("Hello world")

    assert isinstance(vector, list)
    assert len(vector) > 0

def test_embedding_access(processed_file, logged_in_user):
    vectors = get_embeddings_by_upload(
        processed_file["id"],
        processed_file["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(vectors) > 0

def test_other_user_embedding_access(processed_file, second_logged_in_user):
    vectors = get_embeddings_by_upload(
        processed_file["id"],
        processed_file["notebook_id"],
        second_logged_in_user["user_id"]
    )

    assert len(vectors) == 0

def test_embedding_matches_chunk_count(processed_file, logged_in_user):
    chunks = get_chunks_by_upload(
        processed_file["id"],
        processed_file["notebook_id"],
        logged_in_user["user_id"]
    )

    embeddings = get_embeddings_by_upload(
        processed_file["id"],
        processed_file["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(chunks) == len(embeddings)