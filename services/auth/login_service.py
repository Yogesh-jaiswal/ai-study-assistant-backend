import logging
from app.extensions import db
from models import User

from exceptions import AuthenticationError

from services.auth.password_service import verify_password
from services.auth.jwt_service import create_access_token
from configs.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

def login_user(payload):
    """Check credententials and generate access token for user"""
    user = db.session.query(User).filter_by(email=payload.email).first()

    if user:
        is_password_ok = verify_password(payload.password, user.password_hash)
    else: # Prevents malicious attacks
        is_password_ok = verify_password(payload.password, settings.DUMMY_HASH)

    if not user or not is_password_ok:
        logger.warning(f"Invalid login attempt for email {payload.email}")
        raise AuthenticationError("Invalid Credentials")
    
    access_token = create_access_token(user.id)

    return access_token