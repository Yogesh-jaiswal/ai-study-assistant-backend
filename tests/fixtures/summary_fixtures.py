from pytest import fixture

@fixture()
def generated_summary(uploaded_file):
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

    assert response.status_code == 201

    return {
        "id": response.get_json()["id"],
        "notebook_id": uploaded_file["notebook_id"],
        "client": client,
        "access_token": uploaded_file["access_token"]
    }

@fixture()
def second_generated_summary(second_uploaded_file):
    client = second_uploaded_file["client"]

    response = client.post(
        f"/v1/notebooks/{second_uploaded_file['notebook_id']}/summaries",
        json = {
            "upload_ids": [second_uploaded_file["id"]]
        },
        headers={
            "Authorization": f"Bearer {second_uploaded_file['access_token']}"
        }
    )

    assert response.status_code == 201

    return {
        "id": response.get_json()["id"],
        "notebook_id": second_uploaded_file["notebook_id"],
        "client": client,
        "access_token": second_uploaded_file["access_token"]
    }