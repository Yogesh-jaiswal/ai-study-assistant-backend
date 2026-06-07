import uuid
import jwt
from typing import Any

from datetime import datetime, timedelta, timezone

from configs import settings

def create_access_token(user_id: int) -> str:
    """
    Function to generate a new JWT access token
    """
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)
    }

    return jwt.encode(
        payload,
        settings.jwt_private_key,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Function to decode the existing JWT token
    """
    return jwt.decode(
        token,
        settings.jwt_public_key,
        algorithms=[settings.JWT_ALGORITHM],
        options={
            "require": [
                "sub",
                "jti",
                "iat",
                "nbf",
                "exp"
            ]
        },
        leeway=30
    )