from pytest import fixture

from tests.builders.ai_content_builder import AIContentBuilder


@fixture
def ai_content_builder(client):
    return AIContentBuilder(client)


def create_ai_content(builder, upload, endpoint_key: str, result_key: str, payload: dict) -> dict:
    ai_content = builder.generate(
        endpoint=f"/v1/notebooks/{upload['notebook_id']}/{endpoint_key}",
        access_token=upload["access_token"],
        payload=payload,
        result_key=result_key,
    )

    return {
        **upload,
        **ai_content,
    }


@fixture
def generated_summary(
    ai_content_builder,
    completed_upload,
):
    payload={
        "upload_ids": [
            completed_upload["upload_id"]
        ]
    }

    return create_ai_content(ai_content_builder, completed_upload, "summaries", "summary_id", payload)


@fixture
def second_generated_summary(
    ai_content_builder,
    second_completed_upload,
):
    payload={
        "upload_ids": [
            second_completed_upload["upload_id"]
        ]
    }

    return create_ai_content(ai_content_builder, second_completed_upload, "summaries", "summary_id", payload)

@fixture
def generated_exam(
    ai_content_builder,
    completed_upload,
):
    payload={
        "upload_ids": [
            completed_upload["upload_id"]
        ],
        "difficulty": "easy",
        "exam_type": "quiz"
    }

    return create_ai_content(ai_content_builder, completed_upload, "exams", "exam_id", payload)

@fixture
def second_generated_exam(
    ai_content_builder,
    second_completed_upload,
):
    payload={
        "upload_ids": [
            second_completed_upload["upload_id"]
        ],
        "difficulty": "easy",
        "exam_type": "quiz"
    }

    return create_ai_content(ai_content_builder, second_completed_upload, "exams", "exam_id", payload)