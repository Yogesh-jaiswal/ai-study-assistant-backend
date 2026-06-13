import os

os.environ["ENVIRONMENT"] = "testing"

from pytest import fixture
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.extensions import db


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
def session(app):
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

pytest_plugins = [
    "tests.fixtures.auth_fixtures",
    "tests.fixtures.notebook_fixtures",
    "tests.fixtures.upload_fixtures",
    "tests.fixtures.summary_fixtures"
]