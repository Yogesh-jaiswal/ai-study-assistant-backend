from pytest import fixture

from app.factory import create_app
from app.extensions import db
from app.commands.seed_blueprints import seed_exam_blueprints


@fixture(scope="session")
def app():
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
    return app.test_client()