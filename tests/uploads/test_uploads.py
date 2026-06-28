import time
from uuid import uuid4
from io import BytesIO

import pytest

fake_id = str(uuid4())

def test_upload_file(created_notebook):
    """
    User can upload a file inside a notebook successfully.
    """
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        data={
            "files": (
                BytesIO(
                    b"Recursion is a function which calls itself"
                ),
                "Recursion.txt"
            )
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert len(data) == 1

    assert "upload_id" in data[0]
    assert "task_id" in data[0]

def test_upload_to_other_users_notebook(
        created_notebook,
        second_created_notebook
):
    """
    Another user must not upload to another user's notebook.
    """
    client = second_created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        data={
            "files": (
                BytesIO(
                    b"Recursion is a function which calls itself"
                ),
                "Recursion.txt"
            )
        },
        headers={
            "Authorization": f"Bearer {second_created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 404

def test_upload_nonexistent_notebook(logged_in_user):
    """
    Upload on non existent notebook must not work.
    """
    client = logged_in_user["client"]

    response = client.post(
        f"/v1/notebooks/{fake_id}/uploads",
        data={
            "files": (
                BytesIO(
                    b"Recursion is a function which calls itself"
                ),
                "Recursion.txt"
            )
        },
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 404

def test_get_upload(processed_file):
    """
    User must get the uploaded file.
    """
    client = processed_file["client"]

    response = client.get(
        f"/v1/notebooks/{processed_file['notebook_id']}/uploads/{processed_file['id']}",
        headers={
            "Authorization": f"Bearer {processed_file['access_token']}"
        }
    )

    assert response.status_code == 200

def test_get_other_users_upload(
        second_processed_file,
        processed_file
):
    """
    User must not get another user's uploaded file.
    """
    client = second_processed_file["client"]

    response = client.get(
        f"/v1/notebooks/{processed_file['notebook_id']}/uploads/{processed_file['id']}",
        headers={
            "Authorization": f"Bearer {second_processed_file['access_token']}"
        }
    )

    assert response.status_code == 404

@pytest.mark.async_test
def test_get_unprocessed_upload(uploaded_file):
    """
    User must not access upload content before processing finishes.
    """
    client = uploaded_file["client"]

    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 400

def test_get_all_uploads(uploaded_file):
    """
    User should see all the uploaded files.
    """
    client = uploaded_file["client"]

    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["uploads"]) == 1

def test_get_empty_uploads(created_notebook):
    """
    New user should see empty uploaded files list.
    """
    client = created_notebook["client"]

    response = client.get(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["uploads"]) == 0

def test_delete_upload(uploaded_file):
    """
    Owner can delete uplaoded files.
    """
    client = uploaded_file["client"]

    response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 204

def test_delete_other_users_upload(
        second_uploaded_file,
        uploaded_file
):
    """
    Deleting unknown user's uploaded file should return 404.
    """
    client = second_uploaded_file["client"]

    response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {second_uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 404

def test_upload_unsupported_file_type(created_notebook):
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        data={
            "files": (
                BytesIO(b"hello"),
                "malware.exe"
            )
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

def test_upload_without_file(created_notebook):
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

def test_multiple_file_upload(created_notebook):
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        data={
            "files": [
                (
                    BytesIO(b"file 1"),
                    "one.txt"
                ),
                (
                    BytesIO(b"file 2"),
                    "two.txt"
                )
            ]
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert len(data) == 2

def test_other_user_cannot_view_upload_task(
    uploaded_file,
    second_logged_in_user
):
    client = second_logged_in_user["client"]

    response = client.get(
        f"/v1/tasks/{uploaded_file['task_id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404

@pytest.mark.async_test
def test_delete_upload_while_processing(uploaded_file):
    """
    Upload can be deleted while processing is running.
    Task should not crash.
    """
    client = uploaded_file["client"]

    delete_response = client.delete(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
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

    # Upload must stay deleted
    get_response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert get_response.status_code == 404