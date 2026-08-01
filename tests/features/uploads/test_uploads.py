import time
from pathlib import Path
from uuid import uuid4

import pytest

fake_id = str(uuid4())

RESOURCE_DIR = (
    Path(__file__).parents[2]
    / "resources"
    / "uploads"
)

SAMPLE_FILE = RESOURCE_DIR / "sample.md"
ONE_FILE = RESOURCE_DIR / "one.txt"
TWO_FILE = RESOURCE_DIR / "two.txt"
MALWARE_FILE = RESOURCE_DIR / "malware.exe"


def test_upload_file(client, created_notebook):
    """
    User can upload a file inside a notebook successfully.
    """
    with open(SAMPLE_FILE, "rb") as file:
        response = client.post(
            f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
            data={
                "files": (file, SAMPLE_FILE.name)
            },
            headers={
                "Authorization": f"Bearer {created_notebook['access_token']}"
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert len(data) == 1
    assert "upload_id" in data[0]
    assert "task_id" in data[0]


def test_upload_to_other_users_notebook(
    client,
    created_notebook,
    second_created_notebook,
):
    """
    Another user must not upload to another user's notebook.
    """
    with open(SAMPLE_FILE, "rb") as file:
        response = client.post(
            f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
            data={
                "files": (file, SAMPLE_FILE.name)
            },
            headers={
                "Authorization": f"Bearer {second_created_notebook['access_token']}"
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 404


def test_upload_nonexistent_notebook(client, logged_in_user):
    """
    Upload on non existent notebook must not work.
    """
    with open(SAMPLE_FILE, "rb") as file:
        response = client.post(
            f"/v1/notebooks/{fake_id}/uploads",
            data={
                "files": (file, SAMPLE_FILE.name)
            },
            headers={
                "Authorization": f"Bearer {logged_in_user['access_token']}"
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 404


def test_get_upload(client, completed_upload):
    """
    User must get the uploaded file.
    """
    response = client.get(
        f"/v1/notebooks/{completed_upload['notebook_id']}/uploads/{completed_upload['upload_id']}",
        headers={
            "Authorization": f"Bearer {completed_upload['access_token']}"
        },
    )

    assert response.status_code == 200


def test_get_other_users_upload(
    client,
    second_completed_upload,
    completed_upload,
):
    """
    User must not get another user's uploaded file.
    """
    response = client.get(
        f"/v1/notebooks/{completed_upload['notebook_id']}/uploads/{completed_upload['upload_id']}",
        headers={
            "Authorization": f"Bearer {second_completed_upload['access_token']}"
        },
    )

    assert response.status_code == 404


@pytest.mark.async_test
def test_get_unprocessed_upload(client, uploaded_file):
    """
    User must not access upload content before processing finishes.
    """
    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['upload_id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        },
    )

    assert response.status_code == 409


def test_get_all_uploads(client, uploaded_file):
    """
    User should see all uploaded files.
    """
    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["uploads"]) == 1


def test_get_empty_uploads(client, created_notebook):
    """
    New notebook should return an empty upload list.
    """
    response = client.get(
        f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["uploads"]) == 0


def test_delete_upload(client, uploaded_file):
    """
    Owner can delete uploaded files.
    """
    response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['upload_id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        },
    )

    assert response.status_code == 204


def test_delete_other_users_upload(
    client,
    second_uploaded_file,
    uploaded_file,
):
    """
    Another user must not delete uploaded files.
    """
    response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['upload_id']}",
        headers={
            "Authorization": f"Bearer {second_uploaded_file['access_token']}"
        },
    )

    assert response.status_code == 404


def test_upload_unsupported_file_type(client, created_notebook):
    """
    Unsupported extensions should be rejected.
    """
    with open(MALWARE_FILE, "rb") as file:
        response = client.post(
            f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
            data={
                "files": (file, MALWARE_FILE.name)
            },
            headers={
                "Authorization": f"Bearer {created_notebook['access_token']}"
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 400


def test_upload_without_file(client, created_notebook):
    """
    Missing multipart file should return 400.
    """
    response = client.post(
        f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400


def test_multiple_file_upload(client, created_notebook):
    """
    Multiple files can be uploaded in one request.
    """
    with (
        open(ONE_FILE, "rb") as one,
        open(TWO_FILE, "rb") as two
    ):
        response = client.post(
            f"/v1/notebooks/{created_notebook['notebook_id']}/uploads",
            data={
                "files": [
                    (one, ONE_FILE.name),
                    (two, TWO_FILE.name)
                ]
            },
            headers={
                "Authorization": f"Bearer {created_notebook['access_token']}"
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert len(data) == 2


def test_other_user_cannot_view_upload_task(
    client,
    uploaded_file,
    second_logged_in_user,
):
    """
    Users must not poll another user's upload task.
    """
    response = client.get(
        f"/v1/tasks/{uploaded_file['task_id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404


@pytest.mark.async_test
def test_delete_upload_while_processing(client, uploaded_file):
    """
    Upload can be deleted while processing is running.
    Background task should finish without crashing.
    """
    delete_response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['upload_id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        },
    )

    assert delete_response.status_code == 204

    task_id = uploaded_file["task_id"]

    for _ in range(20):
        poll_response = client.get(
            f"/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {uploaded_file['access_token']}"
            }
        )

        assert poll_response.status_code == 200

        data = poll_response.get_json()["data"]

        if data["status"] in ("SUCCESS", "FAILURE"):
            break

        time.sleep(0.5)

    get_response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['upload_id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert get_response.status_code == 404