from functools import wraps
from flask import g, request
import jwt

from exceptions import AuthenticationError
from services.auth.jwt_service import decode_access_token

def login_required(func):
    """Decorator to check access token validity"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            raise AuthenticationError("Authentication failed")
        
        token = auth_header.split(" ", 1)[1]

        try:
            payload = decode_access_token(token)

            user_id = payload.get("sub")

            if not user_id:
                raise AuthenticationError("Authentication failed")

            g.user_id = int(user_id)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Authentication failed")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Authentication failed")
        
        return func(*args, **kwargs)
    
    return wrapper