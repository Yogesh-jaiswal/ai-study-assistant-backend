import os
from uuid import uuid4
from typing import Any
from pathlib import Path

from werkzeug.utils import secure_filename

from PIL import Image

from models import Upload
from models.enums import ProcessingStatus, FileTypes, UploadPurpose
from repositories.notebook_repository import get_notebook_by_notebook_id
from repositories.upload_repository import (
    save_upload,
    get_all_uploads_by_notebook_id,
    get_upload_by_upload_id,
    remove_upload
)
from tasks.processing_task import process_file
from services.integrations.redis_service import set_key
from configs import get_settings

from exceptions import ResourceNotFoundError, ConflictError, UnsupportedFileTypeError, BadRequestError

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

def upload_file(notebook_id: str, user_id: str, file, upload_purpose: UploadPurpose) -> dict[str, str]:
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

    relative_path = os.path.join(
        str(notebook.id),
        f"{uuid4()}_{filename}"
    )

    absolute_path = os.path.join(settings.UPLOAD_FOLDER, relative_path)

    file.save(absolute_path)

    upload = Upload(
        notebook_id=notebook_id, 
        filename=filename, 
        upload_purpose=upload_purpose,
        source_type=source_type, 
        processing_status=ProcessingStatus.PENDING, 
        file_path=relative_path # Store relative paths instead of absolute ones so uploads remain portable across local development, Docker, and production deployments.
    )

    save_upload(upload)

    task = process_file.delay(notebook_id, user_id, upload.id)

    # Celery runs outside the request context.
    # Store task ownership in Redis so polling endpoints can
    # later verify task ownership without Flask's g object.
    set_key(
        f"task:{task.id}:owner",
        user_id,
        86400
    )

    set_key(
        f"task:{task.id}:type",
        f"{upload_purpose} upload",
        86400
    )

    return {
        "upload_id": upload.id,
        "task_id": task.id
    }

def get_all_uploads(notebook_id: str, user_id: str, purpose: UploadPurpose | None = None, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    """Retrieves all uploads for a notebook."""
    uploads = get_all_uploads_by_notebook_id(notebook_id, user_id, purpose, limit, offset)
    
    return [
        {
            "id": upload.id,
            "filename": upload.filename,
            "author": upload.author,
            "source_type": upload.source_type.value,
            "upload_purpose": upload.upload_purpose.value,
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
    
    if upload.processing_status == ProcessingStatus.FAILED:
        raise ConflictError("File processing failed can't access it.")
    elif upload.processing_status != ProcessingStatus.COMPLETED:
        raise ConflictError("File is still processing, please wait!")
    
    return {
        "id": upload.id,
        "filename": upload.filename,
        "author": upload.author,
        "source_type": upload.source_type.value,
        "upload_purpose": upload.upload_purpose.value,
        "processing_status": upload.processing_status.value,
        "raw_text": upload.raw_text,
        "uploaded_at": upload.uploaded_at.isoformat()
    }

def preview_file(notebook_id: str, user_id: str, upload_id: str) -> Path:
    """Returns a specific file from the notebook to preview."""
    upload = get_upload_by_upload_id(
        notebook_id,
        user_id,
        upload_id
    )
    if not upload:
        raise ResourceNotFoundError(f"Upload with id {upload_id} not found in notebook {notebook_id}")

    if upload.source_type == FileTypes.YOUTUBE:
        raise BadRequestError("YouTube videos cannot be previewed as files.")
    
    path = Path(settings.UPLOAD_FOLDER).resolve() / upload.file_path

    if not path.exists():
        raise ResourceNotFoundError(f"File not found")
    
    return path

def delete_upload(notebook_id: str, user_id: str, upload_id: str) -> None:
    """Deletes a specific upload for a notebook."""
    upload = get_upload_by_upload_id(
        notebook_id,
        user_id,
        upload_id
    )
    if not upload:
        raise ResourceNotFoundError(f"Upload with id {upload_id} not found in notebook {notebook_id}")
    
    path = Path(settings.UPLOAD_FOLDER).resolve() / upload.file_path

    if path.exists():
        os.remove(path)

    remove_upload(upload)