from typing import Any
from dataclasses import asdict

from models.enums import AIContentTypes
from exceptions import ResourceNotFoundError
from repositories.notebook_repository import get_notebook_by_notebook_id
from repositories.ai_content_repository import (
    get_all_ai_contents_by_notebook_id,
    get_ai_content_by_content_id,
    remove_ai_content
)
from tasks.ai_content_task import create_ai_content
from services.integrations.redis_service import set_key
from services.ai_generation.generation_context import GenerationContext
from services.ai_generation.generation_validator import GenerationValidator

def enqueue_ai_content_generation(
        notebook_id: str, 
        user_id: str, 
        generation_context: GenerationContext,
        content_type: AIContentTypes,
        generation_options: dict
    ) -> str:
    """
    Runs a background task to generate ai content for the specified 
    notebook based on the provided ai generation context and save it.
    """
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError("Notebook not found")

    GenerationValidator.validate(generation_context, notebook_id, user_id)            

    task = create_ai_content.delay(content_type, generation_options, notebook.id, asdict(generation_context), user_id)

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
        f"{content_type} generation",
        86400
    )
    
    return task.id

def get_all_ai_content(notebook_id: str, user_id: str, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    """Retrieves all ai content for a notebook."""
    ai_contents = get_all_ai_contents_by_notebook_id(notebook_id, user_id, limit, offset)
    
    return [
        {
            "id": ai_content.id,
            "title": ai_content.title,
            "type": ai_content.content_type,
            "upload_count": ai_content.upload_count,
            "generated_at": ai_content.generated_at.isoformat()
        } for ai_content in ai_contents
    ]

def get_ai_content(notebook_id: str, user_id: str, ai_content_id: str) -> dict[str, Any]:
    """Retrieves a specific ai content for a notebook."""
    ai_content = get_ai_content_by_content_id(notebook_id, user_id, ai_content_id)
    if not ai_content:
        raise ResourceNotFoundError(f"AI content with id {ai_content_id} not found in notebook {notebook_id}")
    
    return {
        "id": ai_content.id,
        "title": ai_content.title,
        "type": ai_content.content_type,
        "content": ai_content.content,
        "upload_count": ai_content.upload_count,
        "generated_at": ai_content.generated_at.isoformat()
    }

def delete_ai_content(notebook_id: str, user_id: str, ai_content_id: str) -> None:
    """Deletes a specific ai content for a notebook."""
    ai_content = get_ai_content_by_content_id(notebook_id, user_id, ai_content_id)
    if not ai_content:
        raise ResourceNotFoundError(f"AI content with id {ai_content_id} not found in notebook {notebook_id}")

    remove_ai_content(ai_content)