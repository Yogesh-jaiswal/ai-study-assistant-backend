from pydantic import BaseModel, Field, EmailStr
from validators import UpdatedBaseModel

class LoginRequest(UpdatedBaseModel):
    """Schema for login a user"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    
class LoginResponse(BaseModel):
    """Schema for the response when logging in a user"""
    access_token: str = Field(..., description="User's JWT access tokenf")
    expires_in: int = Field(..., description="access token expiration time in seconds")
    message: str = Field(..., description="Success message for login")

class LogoutResponse(BaseModel):
    """Schema for the response when logging out a user"""
    message: str = Field(..., description="Success message for logout")