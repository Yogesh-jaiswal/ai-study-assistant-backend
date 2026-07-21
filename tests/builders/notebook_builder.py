class NotebookBuilder:
    """Build notebook resources."""

    def __init__(self, client):
        self.client = client

    def create(self, access_token: str, title: str):
        response = self.client.post(
            "/v1/notebooks",
            json={
                "title": title
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        assert response.status_code == 201

        return {
            "notebook_id": response.get_json()["data"]["id"]
        }