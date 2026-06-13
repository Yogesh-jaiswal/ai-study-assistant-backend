import uuid

fake_id = str(uuid.uuid4())

def test_upload_file(created_notebook):
    """
    User can upload a file inside a notebook successfully.
    """
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        json = {
            "filename": "Recursion.txt",
            "source_type": "txt",
            "raw_text": "Recursion is a function which calls itself either directly or indirectly"
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 201

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
        json = {
            "filename": "Recursion.txt",
            "source_type": "txt",
            "raw_text": "Recursion is a function which calls itself either directly or indirectly"
        },
        headers={
            "Authorization": f"Bearer {second_created_notebook['access_token']}"
        }
    )

    assert response.status_code == 404

def test_upload_nonexistent_notebook(logged_in_user):
    """
    Upload on non existent notebook must not work.
    """
    client = logged_in_user["client"]

    response = client.post(
        f"/v1/notebooks/{fake_id}/uploads",
        json = {
            "filename": "Recursion.txt",
            "source_type": "txt",
            "raw_text": "Recursion is a function which calls itself either directly or indirectly"
        },
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404

def test_get_upload(uploaded_file):
    """
    User must get the uploaded file.
    """
    client = uploaded_file["client"]

    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 200

def test_get_other_users_upload(
        second_uploaded_file,
        uploaded_file
):
    """
    User must not get another user's uploaded file.
    """
    client = second_uploaded_file["client"]

    response = client.get(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/uploads/{uploaded_file['id']}",
        headers={
            "Authorization": f"Bearer {second_uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 404

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

    data = response.get_json()

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

    data = response.get_json()

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