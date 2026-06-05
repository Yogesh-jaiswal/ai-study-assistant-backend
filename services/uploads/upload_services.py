import logging
from typing import Any

from app.extensions import db
from models import Notebook, Upload
from models.enums import ProcessingStatus
from repositories.notebook_repository import notebook_owned_by_user_query
from validators.upload_schemas import FileUploadRequest

from exceptions import ResourceNotFoundError, DatabaseError

# Set up logging
logger = logging.getLogger(__name__)

def create_upload(notebook_id: int, user_id: int, payload: FileUploadRequest) -> int:
    """Creates a new upload for a notebook."""
    notebook = db.session.scalar(notebook_owned_by_user_query(notebook_id, user_id))
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")

    upload = Upload(
        notebook_id=notebook_id, 
        filename=payload.filename, 
        source_type=payload.source_type, 
        processing_status=ProcessingStatus.COMPLETED, 
        raw_text=payload.raw_text
    )

    db.session.add(upload)
    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Error creating upload for notebook {notebook_id}")
        db.session.rollback()
        raise DatabaseError(f"Failed to create upload")

    return upload.id

def get_all_uploads(notebook_id: int, user_id: int) -> list[dict[str, Any]]:
    """Retrieves all uploads for a notebook."""
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
        .options(db.selectinload(Notebook.uploads))
    )
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

def get_upload(notebook_id: int, user_id: int, upload_id: int) -> dict[str, Any]:
    """Retrieves a specific upload for a notebook."""
    upload = db.session.scalar(
        db.select(Upload)
        .join(Notebook)
        .where(
            Upload.id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
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

def delete_upload(notebook_id: int, user_id: int, upload_id: int) -> None:
    """Deletes a specific upload for a notebook."""
    upload = db.session.scalar(
        db.select(Upload)
        .join(Notebook)
        .where(
            Upload.id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )
    if not upload:
        raise ResourceNotFoundError(f"Upload with id {upload_id} not found in notebook {notebook_id}")

    db.session.delete(upload)
    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Error deleting upload {upload_id} for notebook {notebook_id}")
        db.session.rollback()
        raise DatabaseError(f"Failed to delete upload with id {upload_id}")