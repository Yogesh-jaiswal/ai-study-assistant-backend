from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

from configs import get_settings
from models.enums import FileTypes, ProcessingStatus

from . import UpdatedBaseModel

# Get the settings object
settings = get_settings()

class FileUploadedResponse(BaseModel):
    upload_id: str = Field(..., description="Unique identifier for the uploaded file")
    task_id: str = Field(..., description="Unique identifier for the file processing background task")

class FileMetadataResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the uploaded file")
    filename: str = Field(..., description="Name of the uploaded file")
    source_type: FileTypes = Field(..., description="type of the uploaded file")
    processing_status: ProcessingStatus = Field(..., description="Current processing status of the uploaded file")
    uploaded_at: datetime = Field(..., description="Timestamp of when the file was uploaded")

class GetUploadResponse(FileMetadataResponse):
    raw_text: str = Field(..., description="Extracted raw text content from the uploaded file")

class GetAllUploadsResponse(BaseModel):
    uploads: List[FileMetadataResponse] = Field(..., description="List of all uploads for the notebook")