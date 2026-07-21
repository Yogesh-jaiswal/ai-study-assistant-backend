from tests._helpers.polling import wait_until_success


class TaskBuilder:
    """Builder for task operations."""

    def __init__(self, client):
        self.client = client

    def wait(
        self,
        access_token: str,
        task_id: str,
        timeout: int = 60,
    ):
        return wait_until_success(
            client=self.client,
            access_token=access_token,
            task_id=task_id,
            timeout=timeout,
        )