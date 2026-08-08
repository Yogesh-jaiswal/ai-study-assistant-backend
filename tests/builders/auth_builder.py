class AuthBuilder:
    """Build Authenticated user."""

    def __init__(self, client):
        self.client = client

    def register(self, email: str, username: str, password: str) -> dict:
        response = self.client.post(
            "/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password
            }
        )

        assert response.status_code == 201

        return {
            "user_id": response.get_json()["data"]["id"],
            "email": email,
            "username": username,
            "password": password
        }
    
    def login(self, email: str, password: str)-> dict:
        response = self.client.post(
            "/v1/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 200

        return {
            "access_token": response.get_json()["data"]["access_token"]
        }