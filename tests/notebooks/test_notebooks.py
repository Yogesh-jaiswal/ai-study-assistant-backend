import uuid

fake_id = str(uuid.uuid4())

def test_create_notebook(logged_in_user):
    """
    User can create a notebook successfully.
    """
    client = logged_in_user["client"]

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


def test_create_notebook_invalid_payload(logged_in_user):
    """
    Missing required fields should fail validation.
    """
    client = logged_in_user["client"]

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


def test_get_notebook(created_notebook):
    """
    Notebook owner can retrieve notebook.
    """
    client = created_notebook["client"]

    response = client.get(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200


def test_get_nonexistent_notebook(logged_in_user):
    """
    Unknown notebook should return 404.
    """
    client = logged_in_user["client"]

    response = client.get(
        f"/v1/notebooks/{fake_id}",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_get_other_users_notebook(
    created_notebook,
    second_logged_in_user
):
    """
    User must not access another user's notebook.
    """
    client = second_logged_in_user["client"]

    response = client.get(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_get_all_notebooks(created_notebook):
    """
    User should see created notebooks.
    """
    client = created_notebook["client"]

    response = client.get(
        "/v1/notebooks",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 1


def test_get_all_notebooks_empty(logged_in_user):
    """
    New user should receive empty notebook list.
    """
    client = logged_in_user["client"]

    response = client.get(
        "/v1/notebooks",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 0


def test_delete_notebook(created_notebook):
    """
    Owner can delete notebook.
    """
    client = created_notebook["client"]

    response = client.delete(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 204


def test_deleted_notebook_not_found(created_notebook):
    """
    Deleted notebook should no longer exist.
    """
    client = created_notebook["client"]

    delete_response = client.delete(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert get_response.status_code == 404


def test_delete_other_users_notebook(
    created_notebook,
    second_logged_in_user
):
    """
    User must not delete another user's notebook.
    """
    client = second_logged_in_user["client"]

    response = client.delete(
        f"/v1/notebooks/{created_notebook['id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404


def test_delete_nonexistent_notebook(logged_in_user):
    """
    Deleting unknown notebook should return 404.
    """
    client = logged_in_user["client"]

    response = client.delete(
        f"/v1/notebooks/{fake_id}",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        }
    )

    assert response.status_code == 404