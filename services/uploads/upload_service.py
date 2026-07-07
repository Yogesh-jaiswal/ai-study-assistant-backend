import os
import logging
from uuid import uuid4
from typing import Any
from pathlib import Path

from werkzeug.utils import secure_filename

from PIL import Image

from models import Upload
from models.enums import ProcessingStatus, FileTypes
from repositories.notebook_repository import (
    get_notebook_by_notebook_id,
    get_notebook_with_uploads
)
from repositories.upload_repository import (
    save_upload,
    get_upload_by_upload_id,
    remove_upload
)
from tasks.processing_task import process_file
from services.integrations.redis_service import set_key
from configs import get_settings

from exceptions import ResourceNotFoundError, BadRequestError, UnsupportedFileTypeError

# Set up logging
logger = logging.getLogger(__name__)

# Extension map to get the file type enum based on file extension
EXTENSION_MAP = {
    ".txt": FileTypes.TXT,
    ".pdf": FileTypes.PDF,
    ".md": FileTypes.MARKDOWN,
    ".docx": FileTypes.DOCX,
    ".csv": FileTypes.CSV
}
SUPPORTED_IMAGE_EXTENSIONS = {
    ext.lower() : FileTypes.IMAGE
    for ext, _ in Image.registered_extensions().items()
}

# Settings object
settings = get_settings()

def upload_file(notebook_id: str, user_id: str, file) -> dict[str, str]:
    """Creates a new upload for a notebook."""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if (size > settings.MAX_CONTENT_LENGTH):
        raise BadRequestError("File size is too large.")
    
    filename = secure_filename(file.filename)
    extension = Path(filename).suffix.lower()
    source_type = (
        EXTENSION_MAP.get(extension) 
        or 
        SUPPORTED_IMAGE_EXTENSIONS.get(extension)
    )

    if not source_type:
        raise UnsupportedFileTypeError(f"Unsupported file type {source_type}")

    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")
    
    upload_dir = f"{settings.UPLOAD_FOLDER}/{notebook.id}/"

    # Ensure upload folder exists
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, f"{uuid4()}_{filename}")

    file.save(file_path)

    upload = Upload(
        notebook_id=notebook_id, 
        filename=filename, 
        source_type=source_type, 
        processing_status=ProcessingStatus.PENDING, 
        file_path=file_path
    )

    save_upload(upload)

    task = process_file.delay(notebook_id, user_id, upload.id)

    set_key(
        f"task:{task.id}:owner",
        user_id,
        86400
    )

    set_key(
        f"task:{task.id}:type",
        "upload",
        86400
    )

    return {
        "upload_id": upload.id,
        "task_id": task.id
    }

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
    
    if upload.processing_status != ProcessingStatus.COMPLETED:
        raise BadRequestError("File is still processing")
    
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
    
    if Path(upload.file_path).exists():
       os.remove(upload.file_path)

    remove_upload(upload)