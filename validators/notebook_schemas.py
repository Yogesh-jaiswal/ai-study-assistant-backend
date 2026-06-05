from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

from . import UpdatedBaseModel

class CreateNotebookRequest(UpdatedBaseModel):
    """Schema for creating a notebook."""
    title: str = Field(..., min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value

class NotebookCreatedResponse(BaseModel):
    """Schema for the response when creating a notebook."""
    id: int = Field(...)
    message: str = Field(...)

class GetNotebook(BaseModel):
    """Schema for retrieving a notebook."""
    id: int = Field(...)
    title: str = Field(..., min_length=1, max_length=100)

class GetNotebookMetadata(GetNotebook):
    """Schema for retrieving notebook metadata."""
    created_at: datetime = Field(..., description="Number of summaries associated with the notebook")

class GetAllNotebooksResponse(BaseModel):
    """Schema for the response when retrieving multiple notebooks."""
    data: List[GetNotebookMetadata] = Field(..., min_length=1)