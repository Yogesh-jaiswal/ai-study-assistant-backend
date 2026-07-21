import logging

from app.extensions import db
from models import (
    Notebook,
    AIContent,
    UserAttempt
)
from exceptions import DatabaseError

# Set up logging
logger = logging.getLogger(__name__)


def save_user_attempt(attempt: UserAttempt) -> None:
    """
    Persist a user attempt.

    Raises:
        DatabaseError: If creating the user attempt fails.
    """
    try:
        db.session.add(attempt)
        db.session.commit()

    except Exception:
        logger.exception(
            "Failed creating user attempt"
        )
        db.session.rollback()
        raise DatabaseError(
            "Failed to create user attempt"
        )


def get_all_user_attempt_by_content_id(
        content_id: str,
        notebook_id: str,
        user_id: str,
        limit: int,
        offset: int
) -> list[UserAttempt]:
    """
    Retrieve all attempts under an ai content.

    Returns:
        List of user attempts if ai content found otherwise empty list.
    """

    return db.session.scalars(
        db.select(UserAttempt)
        .join(AIContent)
        .join(Notebook)
        .where(
            UserAttempt.content_id == content_id,
            AIContent.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
        .order_by(
            UserAttempt.evaluated_at.desc()
        )
        .limit(limit)
        .offset(offset)
    ).all()


def get_user_attempt_by_attempt_id(
    attempt_id: str,
    content_id: str,
    notebook_id: str,
    user_id: str
) -> UserAttempt | None:
    """
    Retrieve a user attempt by ID while enforcing notebook ownership.

    Returns:
        The user attempt if found and owned by the user, otherwise None.
    """
    return db.session.scalar(
        db.select(UserAttempt)
        .join(AIContent)
        .join(Notebook)
        .where(
            UserAttempt.id == attempt_id,
            UserAttempt.content_id == content_id,
            AIContent.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )

def update_attempt(attempt: UserAttempt) -> None:
    """
    Update an attempt from the database.

    Raises:
        DatabaseError: If the attempt transaction fails.
    """
    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed to update attempt")
        db.session.rollback()
        raise DatabaseError("Failed to update attempt")