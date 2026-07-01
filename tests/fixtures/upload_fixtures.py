import time
from io import BytesIO
from pytest import fixture

def create_text_file():
    return (
        BytesIO(
            b"""
                Python is a programming language.

                Python supports object oriented programming.

                Python is commonly used with Flask.

                Python has many libraries.



                Paris is the capital of France.

                France is located in Europe.

                Paris has the Eiffel Tower.

                The Seine flows through Paris.



                SQL stores structured information.

                SQL databases use tables.

                Indexes improve query speed.

                SQL supports joins.
            """
        ),
        "Recursion.txt"
    )


def upload_file(created_notebook):
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        data={
            "files": create_text_file()
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 201

    data = response.get_json()["data"][0]

    return {
        "id": data["upload_id"],
        "task_id": data["task_id"],
        "notebook_id": created_notebook["id"],
        "client": client,
        "access_token": created_notebook["access_token"]
    }

def wait_process_file(created_notebook):
    uploaded_data = upload_file(created_notebook)
    client = uploaded_data["client"]
    task_id = uploaded_data["task_id"]

    for _ in range(120):
        polling_response = client.get(
            f"/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {uploaded_data['access_token']}"
            }
        )

        assert polling_response.status_code == 200

        poll_data = polling_response.get_json()

        if poll_data["data"]["status"] == "SUCCESS":
            break
        elif poll_data["data"]["status"] == "FAILURE":
            raise AssertionError (
                f"task failed {task_id}"
            )
        
        time.sleep(0.5)
    else:
        raise AssertionError(
            f"Task {task_id} never completed"
        )

    return {
        "id": uploaded_data["id"],
        "notebook_id": uploaded_data["notebook_id"],
        "client": client,
        "access_token": uploaded_data["access_token"]
    }

@fixture()
def uploaded_file(created_notebook):
    return upload_file(created_notebook)


@fixture()
def second_uploaded_file(second_created_notebook):
    return upload_file(second_created_notebook)

@fixture
def processed_file(created_notebook):
    return wait_process_file(created_notebook)

@fixture
def second_processed_file(second_created_notebook):
    return wait_process_file(second_created_notebook)