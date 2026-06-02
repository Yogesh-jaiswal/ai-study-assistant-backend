import logging

from app.extensions import db
from models import (
    Notebook,
    Upload,
    Summary,
    UploadSummaryRelationship
)
from validators.request_schemas import SummaryRequest
from exceptions import DatabaseError, ResourceNotFoundError
from services.ai.llm_client import generate_response

# Set up logging
logger = logging.getLogger(__name__)

def generate_summary(notebook_id, payload):
    """Generates a summary for the specified notebook based on the provided upload IDs and saves it."""
    notebook = db.session.get(Notebook, notebook_id)
    if not notebook:
        raise ResourceNotFoundError("Notebook not found")

    upload_ids = payload.upload_ids

    uploads = (
        Upload.query
        .options(db.load_only(Upload.id, Upload.raw_text))
        .filter(
            Upload.notebook_id == notebook_id,
            Upload.id.in_(upload_ids)
        )
        .all()
    )
    
    if len(uploads) != len(upload_ids):
        raise ResourceNotFoundError("One or more uploads not found")
    
    title = notebook.title
    content = "\n\n".join(upload.raw_text for upload in uploads if upload.raw_text)

    summary_payload = SummaryRequest(topic=title, notes=content)

    summary_data = generate_response(summary_payload, task="summary")

    try:
        summary = Summary(
            notebook_id=notebook_id,
            summary_data=summary_data,
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

    except Exception as e:
        logger.error(
            f"Failed creating summary for notebook {notebook_id}: {str(e)}"
        )
        db.session.rollback()
        raise DatabaseError(
            "Failed to create summary and relationships"
        ) from e
    
    return summary.id

def get_all_summaries(notebook_id):
    """Retrieves all summaries for a notebook."""
    notebook = (
        db.session.query(Notebook)
        .options(db.selectinload(Notebook.summary))
        .filter(Notebook.id == notebook_id)
        .first()
    )
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")

    summaries = notebook.summary
    
    return [
        {
            "id": summary.id,
            "upload_count": summary.upload_count,
            "generated_at": summary.generated_at.isoformat()
        } for summary in summaries
    ]

def get_summary(notebook_id, summary_id):
    """Retrieves a specific summary for a notebook."""
    summary = (
        db.session.query(Summary)
        .filter(
            Summary.id == summary_id,
            Summary.notebook_id == notebook_id
        )
        .first()
    )
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")
    
    return {
        "id": summary.id,
        "summary_data": summary.summary_data,
        "upload_count": summary.upload_count,
        "generated_at": summary.generated_at.isoformat()
    }

def delete_summary(notebook_id, summary_id):
    """Deletes a specific summary for a notebook."""
    summary = (
        db.session.query(Summary)
        .filter(
            Summary.id == summary_id,
            Summary.notebook_id == notebook_id
        )
        .first()
    )
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")

    db.session.delete(summary)
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error deleting summary {summary_id} for notebook {notebook_id}: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to delete summary with id {summary_id}")