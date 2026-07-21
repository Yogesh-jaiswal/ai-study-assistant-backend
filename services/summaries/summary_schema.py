from pydantic import BaseModel, Field, field_validator

class SummaryResponse(BaseModel):
    """Schema for summary response"""
    title: str = Field(..., description="A short descriptive title summarizing the notes.")
    summary: str = Field(..., min_length=10, description="A concise summary capturing the main ideas from the notes.")
    key_points: list[str] = Field(..., min_length=3, description="A list of the most important points extracted from the notes.")
    important_terms: list[str] = Field(..., min_length=1, description="Important terms, concepts, or keywords that should be remembered.")

    @field_validator("summary")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value