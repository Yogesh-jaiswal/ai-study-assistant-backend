import uuid

fake_id = str(uuid.uuid4())

def test_generate_summary(uploaded_file):
    """
    User must be able to generate summary based on uploaded file.
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

    assert response.status_code == 201

def test_generate_summary_invalid_uploads(uploaded_file):
    """
    User must not be able to generated summary using unexisting file.
    """
    client = uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [fake_id]
        },
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 404

def test_generate_summary_other_users_notebook(
    uploaded_file,
    second_uploaded_file
):
    """
    Another user must not generate summary in someone else's noteboook.
    """
    client = second_uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [uploaded_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {second_uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 404

def test_generate_summary_without_auth(uploaded_file):
    """
    Summary generation requires authentication.
    """
    client = uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json={
            "upload_ids": [uploaded_file["id"]]
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

    data = response.get_json()

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

    data = response.get_json()

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