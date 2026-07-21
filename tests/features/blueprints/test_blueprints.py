from tests.builders.blueprint_builder import BlueprintBuilder

fake_slug = "fake-slug"


def test_create_blueprint(client, logged_in_user):
    response = client.post(
        "/v1/blueprints",
        json=BlueprintBuilder.build_payload(),
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 201

def test_create_blueprint_without_auth(client):
    response = client.post(
        "/v1/blueprints",
        json=BlueprintBuilder.build_payload(),
    )

    assert response.status_code == 401

def test_create_invalid_blueprint(client, logged_in_user):
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
    response = client.get(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {created_blueprint['access_token']}"
        },
    )

    assert response.status_code == 200

def test_get_nonexistent_blueprint(client, logged_in_user):
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
    response = client.get(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_list_my_blueprints(client, created_blueprint):
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
    response = client.get(
        "/v1/blueprints/me",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

    assert response.get_json()["data"]["blueprints"] == []

def test_list_public_blueprints(client, logged_in_user):
    response = client.get(
        "/v1/blueprints",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

    assert len(response.get_json()["data"]["blueprints"]) >= 1

def test_save_public_blueprint(client, logged_in_user):
    response = client.post(
        "/v1/blueprints/standard-school-examination/save",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 200

def test_save_nonexistent_blueprint(client, logged_in_user):
    response = client.post(
        f"/v1/blueprints/{fake_slug}/save",
        headers={
            "Authorization": f"Bearer {logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404

def test_edit_blueprint(client, created_blueprint):
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
    response = client.delete(
        f"/v1/blueprints/{created_blueprint['blueprint_slug']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404