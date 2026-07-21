from models.enums import AIContentTypes

from .response_envelopes import create_success_response
from services.ai_generation.generation_service import (
    enqueue_ai_content_generation
)
from validators.ai_content.basic_schemas import GenerateAIContentResponse
from services.ai_generation.generation_context import GenerationContext

def start_ai_generation(
    notebook_id: str,
    user_id: str,
    generation_context: GenerationContext,
    content_type: AIContentTypes,
    generation_options: dict,
    success_message: str,
):
    """
    Starts an AI content generation task and returns the standardized
    success response containing the created Celery task ID.
    """

    task_id = enqueue_ai_content_generation(
        notebook_id=notebook_id,
        user_id=user_id,
        generation_context=generation_context,
        content_type=content_type,
        generation_options=generation_options,
    )

    return create_success_response(
        GenerateAIContentResponse(
            task_id=task_id,
            message=success_message,
        ).model_dump()
    )