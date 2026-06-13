import logging
from typing import Any

from models import Upload
from models.enums import ProcessingStatus
from repositories.notebook_repository import (
    get_notebook_by_notebook_id,
    get_notebook_with_uploads
)
from repositories.upload_repository import (
    save_upload,
    get_upload_by_upload_id,
    remove_upload
)
from validators.upload_schemas import FileUploadRequest

from exceptions import ResourceNotFoundError, DatabaseError

# Set up logging
logger = logging.getLogger(__name__)

def create_upload(notebook_id: str, user_id: str, payload: FileUploadRequest) -> str:
    """Creates a new upload for a notebook."""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")

    upload = Upload(
        notebook_id=notebook_id, 
        filename=payload.filename, 
        source_type=payload.source_type, 
        processing_status=ProcessingStatus.COMPLETED, 
        raw_text=payload.raw_text
    )

    save_upload(upload)

    return upload.id

def get_all_uploads(notebook_id: str, user_id: str) -> list[dict[str, Any]]:
    """Retrieves all uploads for a notebook."""
    notebook = get_notebook_with_uploads(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")

    uploads = notebook.uploads
    
    return [
        {
            "id": upload.id,
            "filename": upload.filename,
            "source_type": upload.source_type.value,
            "processing_status": upload.processing_status.value,
            "uploaded_at": upload.uploaded_at.isoformat()
        }
        for upload in uploads
    ]

def get_upload(notebook_id: str, user_id: str, upload_id: str) -> dict[str, Any]:
    """Retrieves a specific upload for a notebook."""
    upload = get_upload_by_upload_id(
        notebook_id,
        user_id,
        upload_id
    )
    if not upload:
        raise ResourceNotFoundError(f"Upload with id {upload_id} not found in notebook {notebook_id}")
    
    return {
        "id": upload.id,
        "filename": upload.filename,
        "source_type": upload.source_type.value,
        "processing_status": upload.processing_status.value,
        "raw_text": upload.raw_text,
        "uploaded_at": upload.uploaded_at.isoformat()
    }

def delete_upload(notebook_id: str, user_id: str, upload_id: str) -> None:
    """Deletes a specific upload for a notebook."""
    upload = get_upload_by_upload_id(
        notebook_id,
        user_id,
        upload_id
    )
    if not upload:
        raise ResourceNotFoundError(f"Upload with id {upload_id} not found in notebook {notebook_id}")

    remove_upload(upload)