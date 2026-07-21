import pytest
from repositories.chunk_repository import (
    create_chunk,
    get_chunks_by_upload
)

@pytest.mark.async_test
def test_create_and_get_chunks(
    uploaded_file,
    logged_in_user
):
    upload_id = uploaded_file["upload_id"]

    create_chunk(
        upload_id,
        "chunk one",
        2
    )
    create_chunk(
        upload_id,
        "chunk two",
        3
    )

    chunks = get_chunks_by_upload(
        upload_id,
        uploaded_file["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(chunks) == 2

    assert chunks[0].content == "chunk one"
    assert chunks[1].content == "chunk two"

def test_other_user_cannot_get_chunks(
    completed_upload,
    second_logged_in_user
):
    chunks = get_chunks_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        second_logged_in_user["user_id"]
    )

    assert chunks == []


def test_processing_creates_chunks(
    completed_upload,
    logged_in_user
):

    chunks = get_chunks_by_upload(
        completed_upload["upload_id"],
        completed_upload["notebook_id"],
        logged_in_user["user_id"]
    )

    assert len(chunks) > 0