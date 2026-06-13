import logging
from models import User

from exceptions import AuthenticationError
from repositories.user_repository import get_user_by_email

from validators.auth.login_schemas import LoginRequest

from services.auth.password_service import verify_password
from configs import get_settings

# Get the settings object
settings = get_settings()

# Set up logging
logger = logging.getLogger(__name__)

def login_user(payload: LoginRequest) -> User:
    """Check credententials and generate access token for user"""
    user = get_user_by_email(payload.email)

    if user:
        is_password_ok = verify_password(payload.password, user.password_hash)
    else: # Prevents timing attacks
        is_password_ok = verify_password(payload.password, settings.DUMMY_HASH)

    if not user or not is_password_ok:
        logger.warning(f"Invalid login attempt for email {payload.email}")
        raise AuthenticationError("Invalid Credentials")

    return user