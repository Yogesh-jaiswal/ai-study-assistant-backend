from uuid import uuid4

import pytest

fake_id = str(uuid4())


# ---------------------------------------------------------------------
# Summary Generation
# ---------------------------------------------------------------------

def test_generate_summary(client, completed_upload):
    """
    User can generate a summary from a processed upload.
    """
    response = client.post(
        f"/v1/notebooks/{completed_upload['notebook_id']}/summaries",
        json={
            "upload_ids": [
                completed_upload["upload_id"]
            ]
        },
        headers={
            "Authorization": (
                f"Bearer {completed_upload['access_token']}"
            )
        },
    )


    assert response.status_code == 202

    data = response.get_json()["data"]

    assert "task_id" in data

@pytest.mark.async_test
def test_generate_summary_with_unprocessed_uploads(
    client,
    uploaded_file,
):
    """
    AI content can only be generated from processed uploads.
    """
    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json={
            "upload_ids": [
                uploaded_file["upload_id"]
            ]
        },
        headers={
            "Authorization": (
                f"Bearer {uploaded_file['access_token']}"
            )
        },
    )

    assert response.status_code == 409


def test_generate_summary_other_users_notebook(
    client,
    completed_upload,
    second_completed_upload,
):
    """
    Another user cannot generate AI content in someone else's notebook.
    """
    response = client.post(
        f"/v1/notebooks/{completed_upload['notebook_id']}/summaries",
        json={
            "upload_ids": [
                completed_upload["upload_id"]
            ]
        },
        headers={
            "Authorization": (
                f"Bearer {second_completed_upload['access_token']}"
            )
        },
    )

    assert response.status_code == 404


def test_generate_summary_without_auth(
    client,
    completed_upload,
):
    """
    Summary generation requires authentication.
    """
    response = client.post(
        f"/v1/notebooks/{completed_upload['notebook_id']}/summaries",
        json={
            "upload_ids": [
                completed_upload["upload_id"]
            ]
        },
    )

    assert response.status_code == 401


def test_generate_summary_invalid_uploads(
    client,
    created_notebook,
):
    """
    Unknown uploads should return 404.
    """
    response = client.post(
        f"/v1/notebooks/{created_notebook['notebook_id']}/summaries",
        json={
            "upload_ids": [fake_id]
        },
        headers={
            "Authorization": (
                f"Bearer {created_notebook['access_token']}"
            )
        },
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------
# Generic Content Endpoints
# ---------------------------------------------------------------------

def test_get_content(
    client,
    generated_summary,
):
    """
    User can retrieve generated AI content.
    """
    response = client.get(
        (
            f"/v1/notebooks/{generated_summary['notebook_id']}"
            f"/contents/{generated_summary['summary_id']}"
        ),
        headers={
            "Authorization": (
                f"Bearer {generated_summary['access_token']}"
            )
        },
    )

    assert response.status_code == 200


def test_get_nonexistent_content(
    client,
    created_notebook,
):
    """
    Unknown content should return 404.
    """
    response = client.get(
        (
            f"/v1/notebooks/{created_notebook['notebook_id']}"
            f"/contents/{fake_id}"
        ),
        headers={
            "Authorization": (
                f"Bearer {created_notebook['access_token']}"
            )
        },
    )

    assert response.status_code == 404


def test_get_other_users_content(
    client,
    generated_summary,
    second_generated_summary,
):
    """
    Users cannot access another user's AI content.
    """
    response = client.get(
        (
            f"/v1/notebooks/{generated_summary['notebook_id']}"
            f"/contents/{generated_summary['summary_id']}"
        ),
        headers={
            "Authorization": (
                f"Bearer {second_generated_summary['access_token']}"
            )
        },
    )

    assert response.status_code == 404


def test_get_all_contents(
    client,
    generated_summary,
):
    """
    User should see all generated AI contents.
    """
    response = client.get(
        f"/v1/notebooks/{generated_summary['notebook_id']}/contents",
        headers={
            "Authorization": (
                f"Bearer {generated_summary['access_token']}"
            )
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["ai_contents"]) == 1


def test_get_empty_contents(
    client,
    created_notebook,
):
    """
    New notebook should return an empty content list.
    """
    response = client.get(
        f"/v1/notebooks/{created_notebook['notebook_id']}/contents",
        headers={
            "Authorization": (
                f"Bearer {created_notebook['access_token']}"
            )
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["ai_contents"]) == 0


def test_delete_content(
    client,
    generated_summary,
):
    """
    Owner can delete generated AI content.
    """
    response = client.delete(
        (
            f"/v1/notebooks/{generated_summary['notebook_id']}"
            f"/contents/{generated_summary['summary_id']}"
        ),
        headers={
            "Authorization": (
                f"Bearer {generated_summary['access_token']}"
            )
        },
    )

    assert response.status_code == 204


def test_delete_other_users_content(
    client,
    generated_summary,
    second_generated_summary,
):
    """
    Users cannot delete another user's AI content.
    """
    response = client.delete(
        (
            f"/v1/notebooks/{generated_summary['notebook_id']}"
            f"/contents/{generated_summary['summary_id']}"
        ),
        headers={
            "Authorization": (
                f"Bearer {second_generated_summary['access_token']}"
            )
        },
    )

    assert response.status_code == 404