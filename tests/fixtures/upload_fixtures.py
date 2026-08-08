from pathlib import Path

from pytest import fixture

from tests.builders.upload_builder import UploadBuilder


RESOURCE_DIR = (
    Path(__file__).parents[1]
    / "resources"
    / "uploads"
)


@fixture
def upload_builder(client):
    return UploadBuilder(client)


@fixture
def uploaded_file(
    upload_builder,
    created_notebook,
):
    """Fixture to upload a file for a created notebook."""

    upload = upload_builder.upload(
        notebook_id=created_notebook["notebook_id"],
        access_token=created_notebook["access_token"],
        file_path=RESOURCE_DIR / "sample.md",
    )

    return {
        **created_notebook,
        **upload,
    }


@fixture
def second_uploaded_file(
    upload_builder,
    second_created_notebook,
):
    """Fixture to upload a file for a second created notebook."""

    upload = upload_builder.upload(
        notebook_id=second_created_notebook["notebook_id"],
        access_token=second_created_notebook["access_token"],
        file_path=RESOURCE_DIR / "sample.md",
    )

    return {
        **second_created_notebook,
        **upload,
    }


@fixture
def completed_upload(
    upload_builder,
    uploaded_file,
):
    """Fixture to wait for the completion of an uploaded file."""

    upload_builder.wait(
        access_token=uploaded_file["access_token"],
        task_id=uploaded_file["task_id"]
    )

    return uploaded_file


@fixture
def second_completed_upload(
    upload_builder,
    second_uploaded_file,
):
    """Fixture to wait for the completion of a second uploaded file."""

    upload_builder.wait(
        access_token=second_uploaded_file["access_token"],
        task_id=second_uploaded_file["task_id"]
    )

    return second_uploaded_file