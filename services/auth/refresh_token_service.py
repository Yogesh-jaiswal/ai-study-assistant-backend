import secrets
import hashlib
import logging
from datetime import timezone, datetime

from models import RefreshToken

from exceptions import AuthenticationError, DatabaseError

from app.extensions import db

logger = logging.getLogger(__name__)

def create_refresh_token(user_id: int) -> str:
    token = secrets.token_urlsafe(64)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    db.session.add(RefreshToken(
        user_id=user_id,
        token_hash=token_hash
    ))

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to create refresh token")
        raise DatabaseError("Failed to create refresh token")

    return token

def verify_refresh_token(token: str | None) -> RefreshToken:
    if not token:
        logger.warning("Refresh token not found")
        raise AuthenticationError("Authentication failed")
    
    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    session = db.session.scalar(
        db.select(RefreshToken)
        .where(
            RefreshToken.token_hash == token_hash
        )
    )

    if not session:
        logger.warning("Invalid refresh token")
        raise AuthenticationError("Authentication failed")
    
    expires_at = session.expires_at.replace(
        tzinfo=timezone.utc
    )

    if expires_at < datetime.now(timezone.utc):
        logger.warning("Refresh token expired")
        raise AuthenticationError("Authentication failed, login again")
    
    return session

def revoke_refresh_token(session: RefreshToken) -> None:
    db.session.delete(session)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to revoke refresh token")
        raise DatabaseError("Failed to create refresh token")