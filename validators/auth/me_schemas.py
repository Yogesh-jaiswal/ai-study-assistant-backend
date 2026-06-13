from pydantic import BaseModel, Field, EmailStr

class GetMeResponse(BaseModel):
    """Schema for the response to get the user information"""
    id: str = Field(..., description="Unique identifier for user")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")