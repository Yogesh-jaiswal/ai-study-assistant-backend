from pydantic import Field, field_validator
from typing import List, Literal, Optional
from uuid import UUID

from validators import UpdatedBaseModel

class BaseRequest(UpdatedBaseModel):
    """Base request model for AI content generation requests."""
    upload_ids: List[str] = Field(..., description="Uploads to fetch uploaded files", min_length=1)

    @field_validator("upload_ids")
    @classmethod
    def unique_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("upload_ids must be unique")
        
        for x in v:
            UUID(x)
            
        return v
    
class GenerateSummaryRequest(BaseRequest):
    """Request model for generating a summary from uploaded files."""
    pass

class GenerateQuizRequest(BaseRequest):
    """Request model for generating a quiz from uploaded files."""
    question_count: int = Field(default=5, description="total question count")
    difficulty: Literal["easy", "medium", "hard"] = Field(default="medium", description="quiz difficulty level")
    marks: int = Field(default=1, ge=1, description="marks for each question")
    negative_marking: int = Field(default=0, ge=0, description="negative marking for each wrong answer")

    @field_validator("difficulty")
    @classmethod
    def valid_difficulty(cls, v):
        if v not in ["easy", "medium", "hard"]:
            raise ValueError("difficulty must be in ['easy', 'medium', 'hard]")
        
        return v
    
class GenerateFlashcardsRequest(BaseRequest):
    """Request model for generating flashcards from uploaded files."""
    total_cards: int = Field(..., description="total flashcards to generate")

class GenerateMindMapRequest(BaseRequest):
    """Request model for generating a mind map from uploaded files."""
    pass

class GenerateExamRequest(BaseRequest):
    """Request model for generating an exam from uploaded files."""
    reference_ids: Optional[List[str]] = Field(default=None, description="Uploads to fetch reference files", min_length=1)
    blueprint_slug: Optional[str] = Field(default=None)
    difficulty: Literal["easy", "medium", "hard", "mixed"]
    exam_type: Literal["quiz", "school", "university", "competitive", "certification"]

    @field_validator("reference_ids")
    @classmethod
    def unique_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("reference_ids must be unique")
        
        for x in v:
            UUID(x)
            
        return v