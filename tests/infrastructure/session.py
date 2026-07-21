from pytest import fixture
from app.extensions import db

from tests._helpers.database import reset_database, transaction_session

@fixture()
def session(app, async_tasks):
    if async_tasks:
        reset_database()
        yield db.session

    else:
        with transaction_session() as session:
            yield session