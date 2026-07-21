from pytest import fixture

from app.celery_app import celery_app as celery

from tests._helpers.worker import (
    start_worker,
    wait_until_ready,
    stop_worker,
)


@fixture(scope="session", autouse=True)
def configure_celery(app, async_tasks):
    celery.conf.task_always_eager = not async_tasks
    yield


@fixture(scope="session", autouse=True)
def celery_worker(async_tasks):

    if not async_tasks:
        yield
        return

    worker = start_worker()
    wait_until_ready(worker)

    yield

    stop_worker(worker)