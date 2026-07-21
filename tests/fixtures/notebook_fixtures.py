from pytest import fixture
from tests.builders.notebook_builder import NotebookBuilder

@fixture
def notebook_builder(client):
    return NotebookBuilder(client)


@fixture
def created_notebook(
    notebook_builder,
    logged_in_user
):
    notebook = notebook_builder.create(
        access_token=logged_in_user["access_token"],
        title="My first notebook"
    )

    return {
        **logged_in_user,
        **notebook
    }


@fixture
def second_created_notebook(
    notebook_builder,
    second_logged_in_user
):
    notebook = notebook_builder.create(
        access_token=second_logged_in_user["access_token"],
        title="My first notebook"
    )

    return {
        **second_logged_in_user,
        **notebook
    }