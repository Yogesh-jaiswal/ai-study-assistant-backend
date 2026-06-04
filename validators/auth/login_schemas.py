from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    
class LoginResponse(BaseModel):
    access_token: str = Field(..., description="User's JWT access tokenf")
    expires_in: int = Field(..., description="access token expiration time in seconds")
    message: str = Field(..., description="Success message for login")