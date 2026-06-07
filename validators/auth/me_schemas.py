from pydantic import BaseModel, Field, EmailStr

class GetMeResponse(BaseModel):
    """Schema for the response to get the user information"""
    id: int = Field(..., description="Unique identifier for user")
    email: EmailStr = Field(..., description="User's email address")
    user_name: str = Field(..., description="User's username")