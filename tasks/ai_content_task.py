from redis.exceptions import ConnectionError, TimeoutError

from app.celery_app import celery_app as celery
from services.ai_jobs.job_registry import AI_JOB_REGISTRY
from models import AIContent
from models.enums import AIContentTypes
from repositories.ai_content_repository import save_ai_content
from services.ai_generation.generation_context import GenerationContext
from services.ai_generation.generation_loader import GenerationContextBuilder

@celery.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def create_ai_content(self, content_type: AIContentTypes, generation_options: dict, notebook_id: str, generation_context: dict, user_id: str) -> dict:
    job = AI_JOB_REGISTRY.get(content_type)

    generation_context = GenerationContext(**generation_context)

    if not job:
        raise RuntimeError(f"No AI job registered for {content_type}")
    
    resources = GenerationContextBuilder.build(notebook_id, generation_context, user_id)
    
    content = job.execute(generation_options, resources)
    title = content.get("title")
    ai_content_data = content.copy()
    ai_content_data.pop("title")
    
    ai_content = AIContent(
        notebook_id=notebook_id,
        title=title,
        content_type=content_type,
        upload_count=len(generation_context.note_ids),
        content=ai_content_data
    )

    save_ai_content(ai_content, generation_context.note_ids)

    return {
        "content_id": ai_content.id
    }