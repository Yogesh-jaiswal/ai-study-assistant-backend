from .task_builder import TaskBuilder

class AttemptBuilder(TaskBuilder):

    def __init__(self, client):
        super().__init__(client)

    def create(
        self,
        notebook_id: str,
        content_id: str,
        access_token: str,
        answers: list[dict],
    ):

        response = self.client.post(
            f"/v1/notebooks/{notebook_id}/contents/{content_id}/attempts",
            json={
                "answers": answers
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        assert response.status_code == 202

        data = response.get_json()["data"]

        result = self.wait(
            access_token,
            data["task_id"]
        )

        return {
            "attempt_task_id": data["task_id"],
            "attempt_id": result["result"]["attempt_id"]
        }