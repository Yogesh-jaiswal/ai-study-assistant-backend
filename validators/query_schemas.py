from pydantic import BaseModel, Field, field_validator

from . import UpdatedBaseModel

class QueryRequest(UpdatedBaseModel):
    """Request schema for asking a query."""
    question: str = Field(..., min_length=10, max_length=500)

class QueryResponse(BaseModel):
    """Schema for query response"""
    response: str = Field(..., min_length=10)