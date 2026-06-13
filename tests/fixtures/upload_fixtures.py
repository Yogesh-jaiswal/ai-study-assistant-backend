from pytest import fixture

@fixture()
def uploaded_file(created_notebook):
    client = created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{created_notebook['id']}/uploads",
        json = {
            "filename": "Recursion.txt",
            "source_type": "txt",
            "raw_text": "Recursion is a function which calls itself either directly or indirectly"
        },
        headers={
            "Authorization": f"Bearer {created_notebook['access_token']}"
        }
    )

    assert response.status_code == 201

    return {
        "id": response.get_json()["id"],
        "notebook_id": created_notebook["id"],
        "client": client,
        "access_token": created_notebook["access_token"]
    }

@fixture()
def second_uploaded_file(second_created_notebook):
    client = second_created_notebook["client"]

    response = client.post(
        f"/v1/notebooks/{second_created_notebook['id']}/uploads",
        json = {
            "filename": "Recursion.txt",
            "source_type": "txt",
            "raw_text": "Recursion is a function which calls itself either directly or indirectly"
        },
        headers={
            "Authorization": f"Bearer {second_created_notebook['access_token']}"
        }
    )

    assert response.status_code == 201

    return {
        "id": response.get_json()["id"],
        "client": client,
        "notebook_id": second_created_notebook["id"],
        "access_token": second_created_notebook["access_token"]
    }