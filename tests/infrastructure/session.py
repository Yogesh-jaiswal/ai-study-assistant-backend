from pytest import fixture
from app.extensions import db

from tests._helpers.database import reset_database, transaction_session

@fixture()
def session(app, async_tasks):
    """
    Fixture to provide a database session for testing. 
    It either resets the database and provides a new session if async tasks are enabled, 
    or uses a transaction-based session for synchronous tests.
    """
    if async_tasks:
        reset_database()
        yield db.session

    else:
        with transaction_session() as session:
            yield session