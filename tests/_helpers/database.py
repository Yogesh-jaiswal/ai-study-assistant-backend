import time

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.extensions import db
from app.commands.seed_blueprints import seed_exam_blueprints


def reset_database():
    """
    Reset the PostgreSQL test database by truncating all tables,
    resetting identities, and restoring reference data.
    """
    # Small synchronization delay.
    # Prevents reset_database() from truncating tables while the Celery
    # worker is still releasing its SQLAlchemy session after the previous test.
    # Without this delay intermittent race conditions occurs.
    time.sleep(0.01)
    
    db.session.rollback()

    tables = ", ".join(table.name for table in db.metadata.sorted_tables)

    db.session.execute(
        text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE")
    )
    db.session.commit()

    seed_exam_blueprints()
    db.session.commit()


@contextmanager
def transaction_session():
    """Context manager to create a new database session with a transaction."""
    connection = db.engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    previous_session = db.session
    db.session = session

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        db.session = previous_session