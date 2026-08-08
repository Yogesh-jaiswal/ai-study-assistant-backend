from pydantic import BaseModel, Field

from models.enums import FileTypes

from . import UpdatedBaseModel

class QueryRequest(UpdatedBaseModel):
    """Request schema for asking a query."""
    question: str = Field(..., min_length=10, max_length=500)

class CitationResponse(BaseModel):
    """Schema for citation response"""
    filename: str
    source_type: FileTypes
    author: str | None
    metadata: dict

class QueryResponse(BaseModel):
    """Schema for query response"""
    response: str = Field(..., min_length=10)
    citations: list[CitationResponse] = Field(..., default_factory=list)