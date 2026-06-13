import logging

from models import RefreshToken
from exceptions import DatabaseError
from app.extensions import db

# Set up logging
logger = logging.getLogger(__name__)


def save_refresh_token(refresh_token: RefreshToken) -> None:
    """
    Persist a refresh token to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    db.session.add(refresh_token)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to create refresh token")
        raise DatabaseError("Failed to create refresh token")


def get_refresh_token_by_token_hash(
    token_hash: str
) -> RefreshToken | None:
    """
    Retrieve a refresh token using its hashed value.

    Returns:
        The matching refresh token if found, otherwise None.
    """
    refresh_token = db.session.scalar(
        db.select(RefreshToken)
        .where(
            RefreshToken.token_hash == token_hash
        )
    )

    return refresh_token


def delete_refresh_token(refresh_token: RefreshToken) -> None:
    """
    Delete a refresh token from the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    db.session.delete(refresh_token)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to revoke refresh token")
        raise DatabaseError("Failed to revoke refresh token")