import logging
from typing import Any
from app.extensions import db
from models import User

from exceptions import AuthenticationError

from validators.auth.login_schemas import LoginRequest

from services.auth.password_service import verify_password
from configs import settings

# Set up logging
logger = logging.getLogger(__name__)

def login_user(payload: LoginRequest) -> User:
    """Check credententials and generate access token for user"""
    user = db.session.scalar(
        db.select(User)
        .where(User.email == payload.email.lower())
    )

    if user:
        is_password_ok = verify_password(payload.password, user.password_hash)
    else: # Prevents timing attacks
        is_password_ok = verify_password(payload.password, settings.DUMMY_HASH)

    if not user or not is_password_ok:
        logger.warning(f"Invalid login attempt for email {payload.email}")
        raise AuthenticationError("Invalid Credentials")

    return user