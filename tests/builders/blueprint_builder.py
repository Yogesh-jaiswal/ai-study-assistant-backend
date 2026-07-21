import json
from pathlib import Path


class BlueprintBuilder:
    """Build exam blueprint resources."""

    def __init__(self, client):
        self.client = client

    def create(
        self,
        access_token: str,
        payload: dict,
    ) -> dict:

        response = self.client.post(
            "/v1/blueprints",
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        assert response.status_code == 201

        return {
            "blueprint_slug": response.get_json()["data"]["blueprint_slug"]
        }

    @staticmethod
    def build_payload(is_public: bool = False) -> dict:
        path = (
            Path(__file__).parents[1]
            / "resources"
            / "blueprints"
            / "sample.json"
        )

        payload = {
            "is_public": is_public,
            "structure": json.loads(path.read_text(encoding="utf-8"))
        }

        return payload