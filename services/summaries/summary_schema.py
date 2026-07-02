from pydantic import BaseModel, Field, field_validator

class SummaryResponse(BaseModel):
    """Schema for summary response"""
    summary: str = Field(..., min_length=10)
    key_points: list[str] = Field(..., min_length=3)
    important_terms: list[str] = Field(..., min_length=1)

    @field_validator("summary")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value