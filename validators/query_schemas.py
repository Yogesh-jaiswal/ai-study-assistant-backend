from pydantic import BaseModel, Field, field_validator

from . import UpdatedBaseModel

class QueryRequest(UpdatedBaseModel):
    """Request schema for asking a query."""
    question: str = Field(..., min_length=10, max_length=500)

class QueryServiceRequest(QueryRequest):
    """Schema to pass to the LLM client."""
    context: str = Field(..., min_length=10)

class QueryResponse(BaseModel):
    """Response schema for ask route."""
    response: str = Field(...)