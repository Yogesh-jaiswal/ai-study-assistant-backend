import logging
from pathlib import Path

from sqlalchemy.orm.exc import StaleDataError

from app.celery_app import celery_app as celery
from app.extensions import db
from models.enums import ProcessingStatus
from services.file_processors import FileProcessor
from repositories.upload_repository import update_upload, get_upload_by_upload_id
from repositories.chunk_repository import bulk_create_chunks
from repositories.embedding_repository import bulk_create_embeddings
from configs import get_settings

# Set up logging
logger = logging.getLogger(__name__)

# Settings object
settings = get_settings()

def safe_rollback():
    """
    Function to safely rollback the DB if any failure occurs to prevent race conditions.
    """
    try:
        db.session.rollback()
    except Exception:
        pass

def get_safe_error_message(exc):
    """
    Helper function to create sanitized error messages.
    """
    if isinstance(exc, ValueError):
        return "Invalid file content"

    if isinstance(exc, FileNotFoundError):
        return "Uploaded file not found"

    return "File processing failed"

@celery.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def process_file(self, notebook_id: str, user_id: str, upload_id: str):
    logger.info(
        "Processing upload %s in %s mode",
        upload_id,
        settings.ENVIRONMENT
    )

    upload = get_upload_by_upload_id(
        notebook_id,
        user_id,
        upload_id
    )

    if not upload:
        logger.warning("Upload deleted before processing")
        return

    # Save values we need later
    file_path = upload.file_path
    source_type = upload.source_type

    # Update processing status to processing
    try:
        upload.processing_status = ProcessingStatus.PROCESSING
        update_upload(upload)
    except StaleDataError:
        safe_rollback()
        logger.warning("Upload deleted before processing started")
        return

    if not Path(file_path).exists():

        fresh_upload = get_upload_by_upload_id(
            notebook_id,
            user_id,
            upload_id
        )

        if not fresh_upload:
            return

        # If file doesn't exists set processing status to failed
        try:
            fresh_upload.processing_status = ProcessingStatus.FAILED
            fresh_upload.error_message = "File not found"
            update_upload(fresh_upload)
        except StaleDataError:
            safe_rollback()
            logger.warning("Upload deleted while reporting failure")

        return {
            "upload_id": upload_id,
            "file_status": ProcessingStatus.FAILED
        }

    # Process file
    try:
        processor = FileProcessor(
            source_type,
            test_mode=(settings.ENVIRONMENT == "testing")
        )

        processed_file = processor.process(file_path)

        fresh_upload = get_upload_by_upload_id(
            notebook_id,
            user_id,
            upload_id
        )

        if not fresh_upload:
            logger.warning("Upload deleted during processing")
            return
        
        # Save chunks into the database
        created_chunks = bulk_create_chunks(fresh_upload.id, processed_file.chunks)

        # Save embeddinbgs into the database
        chunk_ids = [chunk.id for chunk in created_chunks]
        bulk_create_embeddings(chunk_ids, processed_file.embeddings)

        # Set file processing status to completed
        fresh_upload.raw_text = processed_file.cleaned_text
        fresh_upload.processing_status = ProcessingStatus.COMPLETED

        db.session.commit() # commit once to prevent race conditions

        return {
            "upload_id": upload_id,
            "file_status": ProcessingStatus.COMPLETED
        }

    except Exception as e:
        logger.exception("File processing failed")
        safe_rollback()

        fresh_upload = get_upload_by_upload_id(
            notebook_id,
            user_id,
            upload_id
        )

        if not fresh_upload:
            logger.warning("Upload deleted during processing")
            return

        # Set file processing status to failed
        try:
            fresh_upload.error_message = get_safe_error_message(e)
            fresh_upload.processing_status = ProcessingStatus.FAILED
            update_upload(fresh_upload)
        except StaleDataError:
            safe_rollback()
            logger.warning("Upload deleted while reporting failure")