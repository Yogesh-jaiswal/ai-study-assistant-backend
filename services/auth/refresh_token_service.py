import secrets
import hashlib
import logging
from datetime import timezone, datetime

from models import RefreshToken

from exceptions import AuthenticationError

from repositories.refresh_token_repository import (
    save_refresh_token,
    get_refresh_token_by_token_hash,
    delete_refresh_token
)

# Set up logging
logger = logging.getLogger(__name__)

def create_refresh_token(user_id: str) -> str:
    token = secrets.token_urlsafe(64)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    save_refresh_token(RefreshToken(
        user_id=user_id,
        token_hash=token_hash
    ))

    return token

def verify_refresh_token(token: str | None) -> RefreshToken:
    if not token:
        logger.warning("Refresh token not found")
        raise AuthenticationError("Authentication failed")
    
    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    session = get_refresh_token_by_token_hash(token_hash)

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
    delete_refresh_token(session)