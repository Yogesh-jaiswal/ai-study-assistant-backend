from pytest import fixture

from tests.builders.attempt_builder import AttemptBuilder
from tests._helpers.exam_answer import build_answers

@fixture
def attempt_builder(client):
    return AttemptBuilder(client)

@fixture
def created_attempt(
    client,
    attempt_builder,
    generated_exam
):
    
    exam  = client.get(
        (
            f"/v1/notebooks/{generated_exam['notebook_id']}"
            f"/contents/{generated_exam['exam_id']}"
        ),
        headers={
            "Authorization": (
                f"Bearer {generated_exam['access_token']}"
            )
        },
    )

    assert exam.status_code == 200

    attempt = attempt_builder.create(
        notebook_id=generated_exam["notebook_id"],
        content_id=generated_exam["exam_id"],
        access_token=generated_exam["access_token"],
        answers=build_answers(
            exam.get_json()["data"]["content"]
        ),
    )

    return {
        **generated_exam,
        **attempt,
    }