import uuid

fake_id = str(uuid.uuid4())

def test_create_notebook(client, logged_in_user):
    """
    User can create a notebook successfully.
    """
    response = client.post(
        "/v1/notebooks",
        json={
            "title": "My first notebook"
        },
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 201


def test_create_notebook_without_auth(client):
    """
    Protected route should reject anonymous users.
    """
    response = client.post(
        "/v1/notebooks",
        json={
            "title": "My first notebook"
        }
    )

    assert response.status_code == 401


def test_create_notebook_invalid_payload(client, logged_in_user):
    """
    Missing required fields should fail validation.
    """
    response = client.post(
        "/v1/notebooks",
        json={
            "name": "Wrong field"
        },
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 422


def test_get_notebook(client, created_notebook):
    """
    Notebook owner can retrieve notebook.
    """
    response = client.get(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200


def test_get_nonexistent_notebook(client, logged_in_user):
    """
    Unknown notebook should return 404.
    """
    response = client.get(
        f"/v1/notebooks/{fake_id}",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_get_other_users_notebook(
    client,
    created_notebook,
    second_logged_in_user
):
    """
    User must not access another user's notebook.
    """
    response = client.get(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_get_all_notebooks(client, created_notebook):
    """
    User should see created notebooks.
    """
    response = client.get(
        "/v1/notebooks",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["notebooks"]) == 1


def test_get_all_notebooks_empty(client, logged_in_user):
    """
    New user should receive empty notebook list.
    """
    response = client.get(
        "/v1/notebooks",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["notebooks"]) == 0


def test_delete_notebook(client, created_notebook):
    """
    Owner can delete notebook.
    """
    response = client.delete(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 204


def test_deleted_notebook_not_found(client, created_notebook):
    """
    Deleted notebook should no longer exist.
    """
    delete_response = client.delete(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert get_response.status_code == 404


def test_delete_other_users_notebook(
    client,
    created_notebook,
    second_logged_in_user
):
    """
    User must not delete another user's notebook.
    """
    response = client.delete(
        f"/v1/notebooks/{created_notebook['notebook_id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_delete_nonexistent_notebook(client, logged_in_user):
    """
    Deleting unknown notebook should return 404.
    """
    response = client.delete(
        f"/v1/notebooks/{fake_id}",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404