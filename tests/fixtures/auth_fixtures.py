from pytest import fixture


@fixture()
def registered_user(client):
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "john@test.com",
            "username": "John123",
            "password": "John@123"
        }
    )

    assert response.status_code == 201

    return {
        "email": "john@test.com",
        "username": "John123",
        "password": "John@123"
    }


@fixture()
def second_registered_user(client):
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "alice@test.com",
            "username": "Alice123",
            "password": "Alice@123"
        }
    )

    assert response.status_code == 201

    return {
        "email": "alice@test.com",
        "username": "Alice123",
        "password": "Alice@123"
    }


@fixture()
def logged_in_user(client, registered_user):
    response = client.post(
        "/v1/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    assert response.status_code == 200

    return {
        "client": client,
        "email": registered_user["email"],
        "username": registered_user["username"],
        "access_token": response.get_json()["access_token"]
    }


@fixture()
def second_logged_in_user(client, second_registered_user):
    response = client.post(
        "/v1/auth/login",
        json={
            "email": second_registered_user["email"],
            "password": second_registered_user["password"]
        }
    )

    assert response.status_code == 200

    return {
        "client": client,
        "email": second_registered_user["email"],
        "username": second_registered_user["username"],
        "access_token": response.get_json()["access_token"]
    }