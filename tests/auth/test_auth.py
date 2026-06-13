def test_login_flow(client, registered_user):
    """
    Complete authentication flow from login to logout.

    Ensures login, token refresh, protected route access, and logout
    work correctly for a valid user.
    """
    login_response = client.post(
        "/v1/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    assert login_response.status_code == 200
    assert client.get_cookie("refresh_token") is not None

    access_token = login_response.get_json()["access_token"]

    me_response = client.get(
        "/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert me_response.status_code == 200

    data = me_response.get_json()

    assert data["email"] == registered_user["email"]
    assert data["username"] == registered_user["username"]

    refresh_response = client.get("/v1/auth/refresh")

    assert refresh_response.status_code == 200
    assert client.get_cookie("refresh_token") is not None

    access_token = refresh_response.get_json()["access_token"]

    me_response = client.get(
        "/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert me_response.status_code == 200

    data = me_response.get_json()

    assert data["email"] == registered_user["email"]
    assert data["username"] == registered_user["username"]

    logout_response = client.get("/v1/auth/logout")

    assert logout_response.status_code == 200


def test_register_duplicate_email(client, registered_user):
    """
    Expected to return an authentication/validation error.
    """
    response = client.post(
        "/v1/auth/register",
        json={
            "email": registered_user["email"],
            "username": "another-user",
            "password": "Password123!"
        }
    )

    assert response.status_code == 401


def test_register_without_email(client):
    """
    Email is a required field for user registration.
    """
    response = client.post(
        "/v1/auth/register",
        json={
            "username": "john",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_register_invalid_email(client):
    """
    Only properly formatted email addresses should be accepted.
    """
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "invalid",
            "username": "john",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_register_extra_field(client):
    """
    Schema validation should prevent unexpected input fields.
    """
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "john@test.com",
            "username": "john",
            "password": "Password123!",
            "admin": True
        }
    )

    assert response.status_code == 422


def test_login_wrong_password(client, registered_user):
    """
    Authentication should not succeed with invalid credentials.
    """
    response = client.post(
        "/v1/auth/login",
        json={
            "email": registered_user["email"],
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """
    The API should not authenticate unknown accounts.
    """
    response = client.post(
        "/v1/auth/login",
        json={
            "email": "ghost@test.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 401


def test_me_without_token(client):
    """
    Requests without an access token should be rejected.
    """
    response = client.get("/v1/auth/me")

    assert response.status_code == 401


def test_me_with_invalid_token(client):
    """
    Only valid access tokens should grant access.
    """
    response = client.get(
        "/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401


def test_refresh_without_cookie(client):
    """
    Requests without the cookie should be unauthorized.
    """
    response = client.get("/v1/auth/refresh")

    assert response.status_code == 401


def test_logout_without_cookie(client):
    """
    Logout requests without authentication should fail.
    """
    response = client.get("/v1/auth/logout")

    assert response.status_code == 401


def test_refresh_token_rotates(logged_in_user):
    """
    A new refresh token should replace the previous one.
    """
    client = logged_in_user["client"]

    old_cookie = client.get_cookie("refresh_token")

    assert old_cookie is not None

    refresh_response = client.get("/v1/auth/refresh")

    assert refresh_response.status_code == 200

    new_cookie = client.get_cookie("refresh_token")

    assert new_cookie is not None
    assert old_cookie.value != new_cookie.value


def test_refresh_after_logout(logged_in_user):
    """
    Token refresh requests should fail once the user logs out.
    """
    client = logged_in_user["client"]

    logout_response = client.get("/v1/auth/logout")

    assert logout_response.status_code == 200

    refresh_response = client.get("/v1/auth/refresh")

    assert refresh_response.status_code == 401