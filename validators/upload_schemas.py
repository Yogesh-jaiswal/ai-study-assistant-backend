from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

from . import UpdatedBaseModel

from models.enums import FileTypes, ProcessingStatus

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

class YoutubeUploadRequest(UpdatedBaseModel):
    url: str = Field(..., description="youtube video url")

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, value: str):
        parsed = urlparse(value)

        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "m.youtube.com",
        }

        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in allowed_hosts:
            raise ValueError("Invalid YouTube URL")

        return value