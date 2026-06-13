import logging
from pydantic import EmailStr

from app.extensions import db
from models import User
from exceptions import DatabaseError

# Set up logging
logger = logging.getLogger(__name__)


def get_user_by_email(email: EmailStr) -> User | None:
    """
    Retrieve a user by email address.

    Email lookup is performed using a normalized lowercase value.
    """
    user = db.session.scalar(
        db.select(User)
        .where(User.email == email.lower())
    )

    return user


def get_user_by_id(user_id: str) -> User | None:
    """
    Retrieve a user by their unique identifier.

    Returns:
        The user if found, otherwise None.
    """
    user = db.session.get(User, user_id)

    return user


def save_user(user: User) -> None:
    """
    Persist a user to the database.

    Raises:
        DatabaseError: If the registration transaction fails.
    """
    db.session.add(user)

    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Registration failed for {user.email}")
        db.session.rollback()
        raise DatabaseError("Failed to register user")