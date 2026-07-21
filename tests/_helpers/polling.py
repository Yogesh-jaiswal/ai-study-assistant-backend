import time


def wait_until_success(
    client,
    access_token: str,
    task_id: str,
    timeout: int = 60,
    interval: float = 0.5,
):
    """
    Poll a task until it completes successfully.

    Raises
    ------
    AssertionError
        If the task fails or exceeds the timeout.
    """

    attempts = int(timeout / interval)

    for _ in range(attempts):

        response = client.get(
            f"/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        assert response.status_code == 200

        data = response.get_json()["data"]

        if data["status"] == "SUCCESS":
            return data

        if data["status"] == "FAILURE":
            raise AssertionError(
                f"Task {task_id} failed."
            )

        time.sleep(interval)

    raise AssertionError(
        f"Task {task_id} never completed."
    )