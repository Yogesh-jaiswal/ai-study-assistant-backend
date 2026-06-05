import logging
from typing import Any
from pydantic import ValidationError

from app.extensions import db
from models import (
    Notebook,
    Upload,
    Summary,
    UploadSummaryRelationship
)
from validators.summary_schemas import GenerateSummaryRequest
from validators.request_schemas import SummaryRequest
from exceptions import DatabaseError, ResourceNotFoundError, ResponseValidationError
from validators.response_schemas import SummaryResponse
from services.ai.llm_client import generate_response
from repositories.notebook_repository import notebook_owned_by_user_query

# Set up logging
logger = logging.getLogger(__name__)

def generate_summary(notebook_id: int, user_id: int, payload: GenerateSummaryRequest) -> int:
    """Generates a summary for the specified notebook based on the provided upload IDs and saves it."""
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
    )
    if not notebook:
        raise ResourceNotFoundError("Notebook not found")

    upload_ids = payload.upload_ids

    uploads = db.session.scalars(
        db.select(Upload)
        .options(db.load_only(Upload.id, Upload.raw_text))
        .where(
            Upload.notebook_id == notebook_id,
            Upload.id.in_(upload_ids)
        )
    ).all()

    
    if len(uploads) != len(upload_ids):
        raise ResourceNotFoundError("One or more uploads not found")
    
    title = notebook.title
    content = "\n\n".join(upload.raw_text for upload in uploads if upload.raw_text)

    summary_payload = SummaryRequest(topic=title, notes=content)

    # Validate the response against the SummaryResponse schema
    try:
        ai_output = generate_response(summary_payload, task="summary")
        summary_data = SummaryResponse(**ai_output)
    except ValidationError:
        logger.exception("response validation failed")

        raise ResponseValidationError(
            "model response failed"
        )

    try:
        summary = Summary(
            notebook_id=notebook_id,
            summary_data=summary_data.model_dump(),
            upload_count=len(uploads)
        )

        db.session.add(summary)
        db.session.flush()

        relationships = [
            UploadSummaryRelationship(
                upload_id=upload.id,
                summary_id=summary.id
            )
            for upload in uploads
        ]

        db.session.add_all(relationships)

        db.session.commit()

    except Exception:
        logger.exception(
            f"Failed creating summary for notebook {notebook_id}"
        )
        db.session.rollback()
        raise DatabaseError(
            "Failed to create summary and relationships"
        )
    
    return summary.id

def get_all_summaries(notebook_id: int, user_id: int) -> list[dict[str, Any]]:
    """Retrieves all summaries for a notebook."""
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
        .options(db.selectinload(Notebook.summaries))
    )
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")

    summaries = notebook.summaries
    
    return [
        {
            "id": summary.id,
            "upload_count": summary.upload_count,
            "generated_at": summary.generated_at.isoformat()
        } for summary in summaries
    ]

def get_summary(notebook_id: int, user_id: int, summary_id: int) -> dict[str, Any]:
    """Retrieves a specific summary for a notebook."""
    summary = db.session.scalar(
        db.select(Summary)
        .join(Notebook)
        .where(
            Summary.id == summary_id,
            Summary.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")
    
    return {
        "id": summary.id,
        "summary_data": summary.summary_data,
        "upload_count": summary.upload_count,
        "generated_at": summary.generated_at.isoformat()
    }

def delete_summary(notebook_id: int, user_id: int, summary_id: int) -> None:
    """Deletes a specific summary for a notebook."""
    summary = db.session.scalar(
        db.select(Summary)
        .join(Notebook)
        .where(
            Summary.id == summary_id,
            Summary.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")

    db.session.delete(summary)
    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Error deleting summary {summary_id} for notebook {notebook_id}")
        db.session.rollback()
        raise DatabaseError(f"Failed to delete summary with id {summary_id}")