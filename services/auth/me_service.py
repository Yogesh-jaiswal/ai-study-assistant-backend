from models.user import User
from exceptions import AuthenticationError
from app.extensions import db

def get_user(user_id: int) -> User:
    user = db.session.get(User, user_id)

    if not user:
        raise AuthenticationError(f"User not found")
    
    return user