from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from app.extensions import db
from app.commands.seed_blueprints import seed_exam_blueprints


def reset_database():
    db.session.rollback()

    # Delete all rows
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())

    db.session.commit()

    # Restore reference data
    seed_exam_blueprints()

    db.session.commit()


@contextmanager
def transaction_session():
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