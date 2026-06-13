import logging
from typing import Any
from pydantic import ValidationError

from models import Summary
from validators.summary_schemas import GenerateSummaryRequest
from validators.request_schemas import SummaryRequest
from exceptions import ResourceNotFoundError, ResponseValidationError
from validators.response_schemas import SummaryResponse
from services.ai.llm_client import generate_response
from repositories.notebook_repository import (
    get_notebook_by_notebook_id,
    get_notebook_with_summaries
)
from repositories.upload_repository import get_uploads_in_group
from repositories.summary_repository import (
    save_summary,
    get_summary_by_summary_id,
    remove_summary
)

# Set up logging
logger = logging.getLogger(__name__)

def generate_summary(notebook_id: str, user_id: str, payload: GenerateSummaryRequest) -> str:
    """Generates a summary for the specified notebook based on the provided upload IDs and saves it."""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError("Notebook not found")

    upload_ids = payload.upload_ids

    uploads = get_uploads_in_group(upload_ids, notebook_id)
    
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

    summary = Summary(
        notebook_id=notebook_id,
        summary_data=summary_data.model_dump(),
        upload_count=len(uploads)
    )

    save_summary(summary, uploads)
    
    return summary.id

def get_all_summaries(notebook_id: str, user_id: str) -> list[dict[str, Any]]:
    """Retrieves all summaries for a notebook."""
    notebook = get_notebook_with_summaries(notebook_id, user_id)
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

def get_summary(notebook_id: str, user_id: str, summary_id: str) -> dict[str, Any]:
    """Retrieves a specific summary for a notebook."""
    summary = get_summary_by_summary_id(notebook_id, user_id, summary_id)
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")
    
    return {
        "id": summary.id,
        "summary_data": summary.summary_data,
        "upload_count": summary.upload_count,
        "generated_at": summary.generated_at.isoformat()
    }

def delete_summary(notebook_id: str, user_id: str, summary_id: str) -> None:
    """Deletes a specific summary for a notebook."""
    summary = get_summary_by_summary_id(notebook_id, user_id, summary_id)
    if not summary:
        raise ResourceNotFoundError(f"Summary with id {summary_id} not found in notebook {notebook_id}")

    remove_summary(summary)