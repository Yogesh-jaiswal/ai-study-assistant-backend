import uuid

fake_id = str(uuid.uuid4())


def test_create_attempt(created_attempt):
    """
    User should be able to evaluate an exam successfully.
    """
    assert created_attempt["attempt_id"] is not None
    assert created_attempt["attempt_task_id"] is not None


def test_create_attempt_invalid_content(
    client,
    generated_exam,
):
    """
    Creating an attempt for a nonexistent content should fail.
    """
    response = client.post(
        f"/v1/notebooks/{generated_exam['notebook_id']}/contents/{fake_id}/attempts",
        json={
            "answers": []
        },
        headers={
            "Authorization": f"Bearer {generated_exam['access_token']}"
        },
    )

    assert response.status_code == 404


def test_create_attempt_invalid_notebook(
    client,
    generated_exam,
):
    """
    Creating an attempt inside an unknown notebook should fail.
    """
    response = client.post(
        f"/v1/notebooks/{fake_id}/contents/{generated_exam['exam_id']}/attempts",
        json={
            "answers": []
        },
        headers={
            "Authorization": f"Bearer {generated_exam['access_token']}"
        },
    )

    assert response.status_code == 404


def test_create_attempt_other_users_content(
    client,
    generated_exam,
    second_logged_in_user,
):
    """
    Another user must not evaluate someone else's exam.
    """
    response = client.post(
        f"/v1/notebooks/{generated_exam['notebook_id']}/contents/{generated_exam['exam_id']}/attempts",
        json={
            "answers": []
        },
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404


def test_create_attempt_without_auth(
    client,
    generated_exam,
):
    """
    Attempt creation requires authentication.
    """
    response = client.post(
        f"/v1/notebooks/{generated_exam['notebook_id']}/contents/{generated_exam['exam_id']}/attempts",
        json={
            "answers": []
        },
    )

    assert response.status_code == 401


def test_create_attempt_invalid_payload(
    client,
    generated_exam,
):
    """
    Invalid payload should fail validation.
    """
    response = client.post(
        f"/v1/notebooks/{generated_exam['notebook_id']}/contents/{generated_exam['exam_id']}/attempts",
        json={
            "wrong": []
        },
        headers={
            "Authorization": f"Bearer {generated_exam['access_token']}"
        },
    )

    assert response.status_code == 422


def test_get_attempt(
    client,
    created_attempt,
):
    """
    Owner should retrieve the evaluated attempt.
    """
    response = client.get(
        f"/v1/notebooks/{created_attempt['notebook_id']}"
        f"/contents/{created_attempt['exam_id']}"
        f"/attempts/{created_attempt['attempt_id']}",
        headers={
            "Authorization": f"Bearer {created_attempt['access_token']}"
        },
    )

    assert response.status_code == 200


def test_get_nonexistent_attempt(
    client,
    generated_exam,
):
    """
    Unknown attempt should return 404.
    """
    response = client.get(
        f"/v1/notebooks/{generated_exam['notebook_id']}"
        f"/contents/{generated_exam['exam_id']}"
        f"/attempts/{fake_id}",
        headers={
            "Authorization": f"Bearer {generated_exam['access_token']}"
        },
    )

    assert response.status_code == 404


def test_get_other_users_attempt(
    client,
    created_attempt,
    second_logged_in_user,
):
    """
    User must not retrieve another user's attempt.
    """
    response = client.get(
        f"/v1/notebooks/{created_attempt['notebook_id']}"
        f"/contents/{created_attempt['exam_id']}"
        f"/attempts/{created_attempt['attempt_id']}",
        headers={
            "Authorization": f"Bearer {second_logged_in_user['access_token']}"
        },
    )

    assert response.status_code == 404


def test_get_all_attempts(
    client,
    created_attempt,
):
    """
    User should see all attempts for an exam.
    """
    response = client.get(
        f"/v1/notebooks/{created_attempt['notebook_id']}"
        f"/contents/{created_attempt['exam_id']}"
        "/attempts",
        headers={
            "Authorization": f"Bearer {created_attempt['access_token']}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["attempts"]) == 1


def test_get_empty_attempts(
    client,
    generated_exam,
):
    """
    New exam should have no attempts.
    """
    response = client.get(
        f"/v1/notebooks/{generated_exam['notebook_id']}"
        f"/contents/{generated_exam['exam_id']}"
        "/attempts",
        headers={
            "Authorization": f"Bearer {generated_exam['access_token']}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data["attempts"]) == 0