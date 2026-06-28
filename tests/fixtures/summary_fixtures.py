from pytest import fixture
import time

def generate_summary(uploaded_file):
    client = uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{uploaded_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [uploaded_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 202

    task_id = response.get_json()["data"]["task_id"]

    for _ in range(20):
        polling_response = client.get(
            f"/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {uploaded_file['access_token']}"
            }
        )

        assert polling_response.status_code == 200

        poll_data = polling_response.get_json()

        if poll_data["data"]["status"] == "SUCCESS":
            summary_id = poll_data["data"]["result"]["summary_id"]
            break
        elif poll_data["data"]["status"] == "FAILURE":
            raise AssertionError (
                f"task failed {task_id}"
            )
        
        time.sleep(0.5)

    assert summary_id is not None, (
        f"Task {task_id} did not finish in time"
    )

    return {
        "id": summary_id,
        "notebook_id": uploaded_file["notebook_id"],
        "client": client,
        "access_token": uploaded_file["access_token"]
    }

@fixture()
def generated_summary(processed_file):
    return generate_summary(processed_file)

@fixture()
def second_generated_summary(second_processed_file):
    return generate_summary(second_processed_file)