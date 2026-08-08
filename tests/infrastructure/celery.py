from pytest import fixture

from app.celery_app import celery_app as celery

from tests._helpers.worker import (
    start_worker,
    wait_until_ready,
    stop_worker,
)


@fixture(scope="session", autouse=True)
def configure_celery(app, async_tasks):
    """
    Fixture to configure Celery for testing. 
    It sets the task_always_eager configuration based on the async_tasks option, 
    allowing tests to run synchronously or asynchronously as needed.
    """
    celery.conf.task_always_eager = not async_tasks
    yield


@fixture(scope="session", autouse=True)
def celery_worker(async_tasks):
    """
    Fixture to manage the lifecycle of a Celery worker for testing. 
    It starts the worker if async_tasks is enabled, 
    waits until it's ready, and stops it after tests are completed.
    """

    if not async_tasks:
        yield
        return

    worker = start_worker()
    wait_until_ready(worker)

    yield

    stop_worker(worker)