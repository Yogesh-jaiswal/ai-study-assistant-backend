from tests.builders.task_builder import TaskBuilder

class AIContentBuilder(TaskBuilder):
    """Build AI generated resources."""
    def __init__(self, client):
        super().__init__(client)

    def generate(
        self,
        endpoint: str,
        access_token: str,
        payload: dict,
        result_key: str,
    ):

        response = self.client.post(
            endpoint,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        assert response.status_code == 202

        task_id = response.get_json()["data"]["task_id"]

        result = self.wait(
            access_token=access_token,
            task_id=task_id,
        )

        return {
            "task_id": task_id,
            result_key: result["result"]["content_id"]
        }