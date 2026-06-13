import logging
from typing import Any

from models import Summary
from validators.summary_schemas import GenerateSummaryRequest
from exceptions import ResourceNotFoundError
from repositories.notebook_repository import (
    get_notebook_by_notebook_id,
    get_notebook_with_summaries
)
from repositories.upload_repository import get_uploads_in_group
from repositories.summary_repository import (
    get_summary_by_summary_id,
    remove_summary
)
from tasks.summary_tasks import create_summary
from services.integrations.redis_service import set_key

# Set up logging
logger = logging.getLogger(__name__)

def enqueue_summary_generation(notebook_id: str, user_id: str, payload: GenerateSummaryRequest) -> str:
    """Runs a background task to generate summary for the specified notebook based on the provided upload IDs and save it."""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError("Notebook not found")

    upload_ids = payload.upload_ids

    uploads = get_uploads_in_group(upload_ids, notebook_id)
    
    if len(uploads) != len(upload_ids):
        raise ResourceNotFoundError("One or more uploads not found")
    
    title = notebook.title
    content = "\n\n".join(upload.raw_text for upload in uploads if upload.raw_text)

    task = create_summary.delay(title, content, notebook.id, upload_ids)

    set_key(
        f"task:{task.id}:owner",
        user_id,
        86400
    )

    set_key(
        f"task:{task.id}:type",
        "summary",
        86400
    )
    
    return task.id

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