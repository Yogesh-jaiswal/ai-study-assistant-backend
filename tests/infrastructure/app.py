from pytest import fixture

from app.factory import create_app
from app.extensions import db
from app.commands.seed_blueprints import seed_exam_blueprints


@fixture(scope="session")
def app():
    """
    Fixture to create and configure a Flask application for testing. 
    It sets up the application context, initializes the database, seeds exam blueprints, 
    and ensures proper cleanup after tests are completed.
    """
    app = create_app()

    app.config.update(
        TESTING=True
    )

    with app.app_context():
        db.create_all()
        seed_exam_blueprints()

        yield app

        db.session.remove()
        db.drop_all()


@fixture()
def client(app, session):
    """Fixture to provide a test client for the Flask application. It allows tests to make HTTP requests to the application without running a live server."""
    return app.test_client()