from tests.builders.blueprint_builder import BlueprintBuilder

fake_slug = "fake-slug"


def test_create_blueprint(client, logged_in_user):
    """Test creating a blueprint with valid data and authentication."""
    response = client.post(
        "/v1/blueprints",
        json=BlueprintBuilder.build_payload(),
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 201

def test_create_blueprint_without_auth(client):
    """Test creating a blueprint without authentication."""
    response = client.post(
        "/v1/blueprints",
        json=BlueprintBuilder.build_payload(),
    )

    assert response.status_code == 401

def test_create_invalid_blueprint(client, logged_in_user):
    """Test creating a blueprint with invalid data."""
    payload = BlueprintBuilder.build_payload()
    del payload["structure"]["exam_name"]

    response = client.post(
        "/v1/blueprints",
        json=payload,
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 422

def test_get_blueprint(client, created_blueprint):
    """Test retrieving a blueprint by its slug."""
    response = client.get(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {created_blueprint['access_token']}"
        },
    )

    assert response.status_code == 200

def test_get_nonexistent_blueprint(client, logged_in_user):
    """Test retrieving a nonexistent blueprint."""
    response = client.get(
        f"/v1/blueprints/{fake_slug}",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_get_other_users_private_blueprint(
    client,
    created_blueprint,
    second_logged_in_user,
):
    """Test retrieving another user's private blueprint."""
    response = client.get(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_list_my_blueprints(client, created_blueprint):
    """Test listing the blueprints of the authenticated user."""
    response = client.get(
        "/v1/blueprints/me",
        headers={
            "Authorization": f"Bearer {created_blueprint['access_token']}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["blueprints"]) == 1

def test_list_empty_blueprints(client, logged_in_user):
    """Test listing blueprints when the user has none."""
    response = client.get(
        "/v1/blueprints/me",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

    assert response.get_json()["data"]["blueprints"] == []

def test_list_public_blueprints(client, logged_in_user):
    """Test listing public blueprints available to the authenticated user."""
    response = client.get(
        "/v1/blueprints",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

    assert len(response.get_json()["data"]["blueprints"]) >= 1

def test_save_public_blueprint(client, logged_in_user):
    """Test saving a public blueprint for the authenticated user."""
    response = client.post(
        "/v1/blueprints/digital-sat/save",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

def test_save_nonexistent_blueprint(client, logged_in_user):
    """Test saving a nonexistent blueprint for the authenticated user."""
    response = client.post(
        f"/v1/blueprints/{fake_slug}/save",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_edit_blueprint(client, created_blueprint):
    """Test editing a blueprint with valid data and authentication."""
    payload = BlueprintBuilder.build_payload()
    payload["structure"]["exam_name"] = "Updated Exam"

    response = client.patch(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        json=payload,
        headers={
            "Authorization": f"Bearer {created_blueprint['access_token']}"
        },
    )

    assert response.status_code == 200

def test_edit_other_users_blueprint(
    client,
    created_blueprint,
    second_logged_in_user,
):
    """Test editing another user's blueprint, which should not be allowed."""
    payload = BlueprintBuilder.build_payload()

    response = client.patch(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        json=payload,
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_delete_blueprint(client, created_blueprint):
    """Test deleting a blueprint with valid authentication."""
    response = client.delete(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {created_blueprint['access_token']}"
        },
    )

    assert response.status_code == 204

def test_delete_other_users_blueprint(
    client,
    created_blueprint,
    second_logged_in_user,
):
    """Test deleting another user's blueprint, which should not be allowed."""
    response = client.delete(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404