from pydantic import BaseModel, Field, field_validator
from typing import Literal

from configs.settings import settings

class SummaryRequest(BaseModel):
    """Request schema for summary generation."""
    topic: str = Field(..., min_length=1, max_length=100)
    notes: str = Field(..., min_length=10, max_length=settings.MAX_NOTES_LENGTH)

    @field_validator("topic", "notes")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value
    
class QuizRequest(SummaryRequest):
    """Request schema for quiz generation."""
    n: int = Field(default = settings.DEFAULT_QUIZ_COUNT, ge = 1, le = settings.MAX_QUIZ_QUESTIONS)
    level: Literal["easy", "medium", "hard"] = Field(default=settings.DEFAULT_QUIZ_LEVEL)