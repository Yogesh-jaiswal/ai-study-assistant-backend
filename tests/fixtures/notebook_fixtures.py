from pytest import fixture

@fixture()
def created_notebook(logged_in_user):
    client = logged_in_user["client"]
    
    response = client.post(
        "/v1/notebooks",
        json={
            "title": "My first notebook"
        },
        headers={
            "Authorization": f"Bearer {logged_in_user["access_token"]}"
        }
    )

    assert response.status_code == 201

    response_json = response.get_json()

    return {
        "id": response_json["id"],
        "client": client,
        "access_token": logged_in_user["access_token"]
    }

@fixture()
def second_created_notebook(second_logged_in_user):
    client = second_logged_in_user["client"]
    
    response = client.post(
        "/v1/notebooks",
        json={
            "title": "My first notebook"
        },
        headers={
            "Authorization": f"Bearer {second_logged_in_user["access_token"]}"
        }
    )

    assert response.status_code == 201

    response_json = response.get_json()

    return {
        "id": response_json["id"],
        "client": client,
        "access_token": second_logged_in_user["access_token"]
    }