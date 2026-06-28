import os
import shutil
from pathlib import Path

os.environ["ENVIRONMENT"] = "testing"

from pytest import fixture, mark
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.extensions import db
from app.celery_app import celery_app as celery
from configs import get_settings

def pytest_addoption(parser):
    parser.addoption(
        "--async-tasks",
        action="store_true",
        default=False,
        help="Enable/ Disable Async Environment"
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--async-tasks"):
        return

    skip_async = mark.skip(
        reason="Need --async-tasks option to run"
    )

    for item in items:
        if "async_test" in item.keywords:
            item.add_marker(skip_async)

@fixture(scope="session")
def app():
    app = create_app()

    app.config.update(
        TESTING=True
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@fixture()
def session(app, request):

    if request.config.getoption("--async-tasks"):

        try:
            yield db.session
        finally:
            db.session.rollback()

            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())

            db.session.commit()

    else:

        connection = db.engine.connect()
        transaction = connection.begin()

        Session = sessionmaker(bind=connection)
        session = Session()

        previous_session = db.session
        db.session = session

        yield session

        session.close()
        transaction.rollback()
        connection.close()

        db.session = previous_session

@fixture()
def client(app, session):
    return app.test_client()

@fixture(scope="session", autouse=True)
def celery_mode(request):

    async_mode = request.config.getoption("--async-tasks")

    celery.conf.task_always_eager = not async_mode

    yield

@fixture(scope="session", autouse=True)
def cleanup_uploads():
    yield

    upload_dir = Path(get_settings().UPLOAD_FOLDER)

    if upload_dir.exists():
        shutil.rmtree(upload_dir)


pytest_plugins = [
    "tests.fixtures.auth_fixtures",
    "tests.fixtures.notebook_fixtures",
    "tests.fixtures.upload_fixtures",
    "tests.fixtures.summary_fixtures"
]