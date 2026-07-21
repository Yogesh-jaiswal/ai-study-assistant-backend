from pathlib import Path

from tests.builders.task_builder import TaskBuilder


class UploadBuilder(TaskBuilder):
    """Build upload resources."""
    def __init__(self, client):
        super().__init__(client)

    def upload(
        self,
        notebook_id: str,
        access_token: str,
        file_path: Path,
    ):

        with open(file_path, "rb") as file:

            response = self.client.post(
                f"/v1/notebooks/{notebook_id}/uploads",
                data={
                    "files": (file, file_path.name)
                },
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                content_type="multipart/form-data",
            )

        assert response.status_code == 201

        data = response.get_json()["data"][0]

        return {
            "upload_id": data["upload_id"],
            "task_id": data["task_id"],
        }

    def upload_youtube(
        self,
        notebook_id: str,
        access_token: str,
        url: str,
    ):

        response = self.client.post(
            f"/v1/notebooks/{notebook_id}/uploads/youtube",
            json={
                "url": url
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )

        assert response.status_code == 201

        data = response.get_json()["data"]

        return {
            "upload_id": data["upload_id"],
            "task_id": data["task_id"],
        }