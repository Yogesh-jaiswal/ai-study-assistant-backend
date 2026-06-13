from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime
from uuid import UUID

from . import UpdatedBaseModel

class GenerateSummaryRequest(UpdatedBaseModel):
    upload_ids: List[str] = Field(..., description="Uploads to fetch uploaded files", min_length=1)

    @field_validator("upload_ids")
    @classmethod
    def unique_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("upload_ids must be unique")
        
        for x in v:
            UUID(x)
            
        return v

class GenerateSummaryResponse(BaseModel):
    task_id: int = Field(..., description="Unique identifier for the celery background task")
    message: str = Field(..., description="Success message confirming summary generation")

class SummaryMetadataResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the generated summary")
    upload_count: int = Field(..., description="Number of uploads used to generate the summary")
    generated_at: datetime = Field(..., description="Timestamp of when the summary was generated")

class SummaryData(BaseModel):
    """Schema for summary response"""
    summary: str = Field(..., min_length=10)
    key_points: List[str] = Field(..., min_length=3)
    important_terms: List[str] = Field(..., min_length=1)

    @field_validator("summary")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")
        
        return value

class GetSummaryResponse(SummaryMetadataResponse):
    summary_data: SummaryData = Field(..., description="Data of the summary in JSON format")

class GetAllSummariesResponse(BaseModel):
    summaries: List[SummaryMetadataResponse] = Field(..., description="List of all the generated summaries from a notebook")