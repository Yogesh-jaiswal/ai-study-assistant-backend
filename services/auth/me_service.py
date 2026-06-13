from models.user import User
from exceptions import AuthenticationError
from repositories.user_repository import get_user_by_id

def get_user(user_id: str) -> User:
    user = get_user_by_id(user_id)

    if not user:
        raise AuthenticationError(f"User not found")
    
    return user