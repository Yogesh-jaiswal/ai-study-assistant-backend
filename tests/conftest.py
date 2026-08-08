import os
os.environ["ENVIRONMENT"] = "testing"

from pytest import mark

# pytest hooks for enabling/disabling async tests and setting up test profiles
def pytest_addoption(parser):
    parser.addoption(
        "--async-tasks",
        action="store_true",
        default=False,
        help="Enable/ Disable Async Environment"
    )

    parser.addoption(
        "--profile",
        action="store",
        default="testing",
    )

# pytest hook to skip async tests if the --async-tasks option is not provided
def pytest_collection_modifyitems(config, items):
    if config.getoption("--async-tasks"):
        return

    skip_async = mark.skip(
        reason="Need --async-tasks option to run"
    )

    for item in items:
        if "async_test" in item.keywords:
            item.add_marker(skip_async)


pytest_plugins = [
    "tests.infrastructure.app",
    "tests.infrastructure.session",
    "tests.infrastructure.cleanup",
    "tests.infrastructure.profiles",
    "tests.infrastructure.celery",
    "tests.fixtures.auth_fixtures",
    "tests.fixtures.notebook_fixtures",
    "tests.fixtures.upload_fixtures",
    "tests.fixtures.ai_content_fixtures",
    "tests.fixtures.extractor_fixtures",
    "tests.fixtures.blueprint_fixtures",
    "tests.fixtures.attempt_fixtures"
]