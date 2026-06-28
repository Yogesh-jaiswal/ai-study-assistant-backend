import uuid
import time

import pytest

fake_id = str(uuid.uuid4())

def test_generate_summary(processed_file):
    """
    User must be able to generate summary based on uploaded file.
    """
    client = processed_file["client"]

    response = client.post(
        f"/v1/notebooks/{processed_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [processed_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {processed_file['access_token']}"
        }
    )

    assert response.status_code == 202

    task_id = response.get_json()["data"]["task_id"]

    for _ in range(20):
        polling_response = client.get(
            f"/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {processed_file['access_token']}"
            }
        )

        poll_data = polling_response.get_json()["data"]

        if poll_data["status"] == "SUCCESS":
            summary_id = poll_data["result"]["summary_id"]
            break
        elif poll_data["status"] == "FAILURE":
            raise AssertionError (
                f"task failed {task_id}"
            )
        
        time.sleep(0.5)

    assert summary_id is not None, (
        f"Task {task_id} did not finish in time"
    )

def test_generate_summary_invalid_uploads(created_notebook):
    """
    User must not be able to generated summary using unexisting file.
    """
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/summaries",
        json = {
            "upload_ids": [fake_id]
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 404

@pytest.mark.async_test
def test_generate_summary_with_unprocessed_uploads(uploaded_file):
    """
    User must not be able to generated summary using unporcessed files.
    """
    client = uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [uploaded_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 400

def test_generate_summary_other_users_notebook(
    processed_file,
    second_processed_file
):
    """
    Another user must not generate summary in someone else's noteboook.
    """
    client = second_processed_file["client"]

    response = client.post(
        f"/v1/notebooks/{processed_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [processed_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {second_processed_file['access_token']}"
        }
    )

    assert response.status_code == 404

def test_generate_summary_without_auth(processed_file):
    """
    Summary generation requires authentication.
    """
    client = processed_file["client"]

    response = client.post(
        f"/v1/notebooks/{processed_file['notebook_id']}/summaries",
        json={
            "upload_ids": [processed_file["id"]]
        }
    )

    assert response.status_code == 401

def test_get_summary(generated_summary):
    """
    User must get the generated summary.
    """
    client = generated_summary["client"]

    response = client.get(
        f"/v1/notebooks/{generated_summary['notebook_id']}/summaries/{generated_summary['id']}",
        headers={
            "Authorization": f"Bearer {generated_summary['access_token']}"
        }
    )

    assert response.status_code == 200

def test_get_nonexistent_summary(created_notebook):
    """
    Fetching unexistent summary should not work.
    """
    client = created_notebook["client"]

    response = client.get(
        f"/v1/notebooks/{created_notebook['id']}/summaries/{fake_id}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 404

def test_get_other_users_summary(
    generated_summary,
    second_generated_summary
):
    """
    User must not access another user's summary.
    """
    client = second_generated_summary["client"]

    response = client.get(
        f"/v1/notebooks/{generated_summary['notebook_id']}/summaries/{generated_summary['id']}",
        headers={
            "Authorization": f"Bearer {second_generated_summary['access_token']}"
        }
    )

    assert response.status_code == 404

def test_get_all_summaries(generated_summary):
    """
    User should see all the generated summaries.
    """
    client = generated_summary["client"]

    response = client.get(
        f"/v1/notebooks/{generated_summary['notebook_id']}/summaries",
        headers={
            "Authorization": f"Bearer {generated_summary['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["summaries"]) == 1

def test_get_empty_summaries(created_notebook):
    """
    New notebook should return empty summary list.
    """
    client = created_notebook["client"]

    response = client.get(
        f"/v1/notebooks/{created_notebook['id']}/summaries",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["summaries"]) == 0

def test_delete_summary(generated_summary):
    """
    User must be able to delete the generated summary.
    """
    client = generated_summary["client"]

    response = client.delete(
        f"/v1/notebooks/{generated_summary['notebook_id']}/summaries/{generated_summary['id']}",
        headers={
            "Authorization": f"Bearer {generated_summary['access_token']}"
        }
    )

    assert response.status_code == 204

def test_delete_other_users_summary(
    generated_summary,
    second_generated_summary
):
    """
    User must not delete another user's summary.
    """
    client = second_generated_summary["client"]

    response = client.delete(
        f"/v1/notebooks/{generated_summary['notebook_id']}/summaries/{generated_summary['id']}",
        headers={
            "Authorization": f"Bearer {second_generated_summary['access_token']}"
        }
    )

    assert response.status_code == 404