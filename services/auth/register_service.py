import logging

from models import User
from repositories.user_repository import (
    get_user_by_email,
    save_user
)

from validators.auth.register_schamas import RegistrationRequest

from exceptions import AuthenticationError

from services.auth.password_service import hash_password

# Set up logging
logger = logging.getLogger(__name__)

def register_user(payload: RegistrationRequest) -> User:
    """Registers a new user"""
    if get_user_by_email(payload.email):
        logger.warning(f"Registration attempt with existing email: {payload.email.lower()}")
        raise AuthenticationError("Registration failed")

    password_hash = hash_password(payload.password)
    user = User(
        username=payload.username,
        email=payload.email.lower(),
        password_hash=password_hash
    )

    save_user(user)

    return user