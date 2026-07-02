import logging

from redis.exceptions import ConnectionError, TimeoutError

from app.celery_app import celery_app as celery
from services.summaries.summary_generator import SummaryGenerator
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
def create_summary(self, title: str, content: str, notebook_id: str, uploads_ids: list[str]) -> None:
    generator = SummaryGenerator()
    summary_data = generator.generate(topic=title, notes=content)
    
    summary = Summary(
        notebook_id=notebook_id,
        summary_data=summary_data,
        upload_count=len(uploads_ids)
    )

    save_summary(summary, uploads_ids)

    return {
        "summary_id": summary.id
    }