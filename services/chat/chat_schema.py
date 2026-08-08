from pydantic import BaseModel, Field, field_validator

class ChatResponse(BaseModel):
    """Schema for query response."""
    response: str = Field(..., min_length=10)

    @field_validator("response")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value