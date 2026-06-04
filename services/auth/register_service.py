import logging

from app.extensions import db
from models import User

from exceptions import DatabaseError, AuthenticationError

from services.auth.password_service import hash_password

# Set up logging
logger = logging.getLogger(__name__)

def register_user(payload):
    """Registers a new user"""
    if db.session.query(User).filter_by(email=payload.email).first():
        logger.warning(f"Registration attempt with existing email: {payload.email.lower()}")
        raise AuthenticationError("Registration failed")

    password_hash = hash_password(payload.password)
    user = User(
        username=payload.username,
        email=payload.email.lower(),
        password_hash=password_hash
    )

    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Registration failed for {payload.email}: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to register user")
    return user