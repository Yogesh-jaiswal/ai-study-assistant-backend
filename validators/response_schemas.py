from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List

class HealthResponse(BaseModel):
    """Schema for health route response"""
    message: str

class SummaryResponse(BaseModel):
    """Schema for summary response"""
    summary: str = Field(..., min_length=10)
    key_points: List[str] = Field(..., min_length=3)
    important_terms: List[str] = Field(..., min_length=1)

    @field_validator("summary")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("feild cannot be empty")
        
        return value
    
class QuizQuestion(BaseModel):
    """Schema for a single quiz question."""
    question: str = Field(..., min_length=10)
    options: list[str] = Field(..., min_length=4)
    answer: str = Field(..., min_length=1)

class QuizResponse(BaseModel):
    """Schema for quiz response containing multiple quiz questions."""
    questions: list[QuizQuestion] = Field(...)

    @field_validator("questions")
    @classmethod
    def validate_length(cls, value, info: ValidationInfo):
        length = info.context.get("n", 5)

        if len(value) != length:
            raise ValueError(f"At least {length} items required")
        
        return value