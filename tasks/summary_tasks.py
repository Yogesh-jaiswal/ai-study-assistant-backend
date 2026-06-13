import logging

from pydantic import ValidationError
from celery import ConnectionError, TimeoutError

from app.celery_app import celery_app as celery, flask_app
from services.ai.llm_client import generate_response
from validators.request_schemas import SummaryRequest
from validators.response_schemas import SummaryResponse
from exceptions import ResponseValidationError
from models import Summary
from repositories.summary_repository import save_summary

# Set up logging
logger = logging.getLogger(__name__)

@celery.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def create_summary(title: str, content: str, notebook_id: str, uploads_ids: list[str]) -> None:
    with flask_app.app_context():
        payload = SummaryRequest(topic=title, notes=content)

        # Validate the response against the SummaryResponse schema
        try:
            ai_output = generate_response(payload, task="summary")
            summary_data = SummaryResponse(**ai_output)
        except ValidationError:
            logger.exception("Summary response validation failed")

            raise ResponseValidationError(
                "model response failed"
            )
        
        summary = Summary(
            notebook_id=notebook_id,
            summary_data=summary_data.model_dump(),
            upload_count=len(uploads_ids)
        )

        save_summary(summary, uploads_ids)

        return {
            "summary_id": summary.id
        }