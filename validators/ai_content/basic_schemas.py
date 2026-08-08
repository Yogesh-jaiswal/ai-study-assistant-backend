from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from models.enums import AIContentTypes

class GenerateAIContentResponse(BaseModel):
    """Response model for a successful AI content generation request."""
    task_id: str = Field(..., description="Unique identifier for the celery background task")
    message: str = Field(..., description="Success message confirming AI content generation")

class AIContentMetadataResponse(BaseModel):
    """Response model for AI content metadata."""
    id: str = Field(..., description="Unique identifier for the generated AI content")
    title: str = Field(..., description="AI generated title")
    type: AIContentTypes = Field(..., description="Type of the generated AI content")
    upload_count: int = Field(..., description="Number of uploads used to generate the AI content")
    generated_at: datetime = Field(..., description="Timestamp of when the AI content was generated")

class GetAIContentResponse(AIContentMetadataResponse):
    """Response model for retrieving a specific AI content."""
    content: dict = Field(..., description="Content of the AI generated content in JSON format")

class GetAllAIContentsResponse(BaseModel):
    """Response model for listing all AI contents."""
    ai_contents: List[AIContentMetadataResponse] = Field(..., description="List of all the generated ai content from a notebook")