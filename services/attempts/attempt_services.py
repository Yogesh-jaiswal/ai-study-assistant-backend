from typing import Any
from dataclasses import asdict

from models.enums import ProcessingStatus, EvaluationTypes
from models import UserAttempt
from exceptions import ResourceNotFoundError
from repositories.ai_content_repository import get_ai_content_by_content_id
from repositories.user_attempt_repository import (
    get_all_user_attempt_by_content_id,
    get_user_attempt_by_attempt_id,
    save_user_attempt
)
from tasks.user_attempt_task import evaluate_user_attempt
from services.integrations.redis_service import set_key
from .attempt_context import AttemptContext
from .attempt_validator import AttemptValidator
from exceptions import ConflictError, BadRequestError

def create_attempt(
        notebook_id: str, 
        user_id: str, 
        evaluation_context: AttemptContext
    ) -> dict[str, str]:
    """Runs a background task to evaluate ai content for the specified ai content based on the provided attempt context and save it."""
    content = get_ai_content_by_content_id(notebook_id, user_id, evaluation_context.content_id)
    if not content:
        raise ResourceNotFoundError("Content not found")
    
    try:
        evaluation_type = EvaluationTypes(content.content_type.value)
    except ValueError:
        raise BadRequestError("No evaluation exists for this ai content")

    AttemptValidator.validate(evaluation_context, notebook_id, user_id, evaluation_type)   

    attempt = UserAttempt(
        content_id=evaluation_context.content_id,
        status=ProcessingStatus.PENDING,
        evaluation_type=evaluation_type,
        evaluation=evaluation_context.answers
    )

    save_user_attempt(attempt)         

    task = evaluate_user_attempt.delay(evaluation_type, attempt.id, evaluation_context.content_id, notebook_id, user_id, asdict(evaluation_context))

    set_key(
        f"task:{task.id}:owner",
        user_id,
        86400
    )

    set_key(
        f"task:{task.id}:type",
        f"{evaluation_type} evaluation",
        86400
    )
    
    return {
        "attempt_id": attempt.id,
        "task_id": task.id
    }

def get_all_attempts(content_id: str, notebook_id: str, user_id: str, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    """Retrieves all attempts for an ai content."""
    attempts = get_all_user_attempt_by_content_id(content_id, notebook_id, user_id, limit, offset)
    
    return [
        {
            "id": attempt.id,
            "status": attempt.status,
            "total_marks": attempt.total_marks,
            "obtained_marks": attempt.obtained_marks,
            "percentage": attempt.percentage,
            "evaluation_type": attempt.evaluation_type,
            "evaluated_at": attempt.evaluated_at.isoformat()
        } for attempt in attempts
    ]

def get_attempt(attempt_id: str, content_id: str, notebook_id: str, user_id: str) -> dict[str, Any]:
    """Retrieves a specific attempt for an ai content."""
    attempt = get_user_attempt_by_attempt_id(attempt_id, content_id, notebook_id, user_id)
    if not attempt:
        raise ResourceNotFoundError(f"Attempt with id {attempt_id} not found for ai content {content_id}")
    
    if attempt.status == ProcessingStatus.FAILED:
        raise ConflictError("Attempt evaluation failed can not access it")
    elif attempt.status != ProcessingStatus.COMPLETED:
        raise ConflictError("Attempt is still evaluating please wait!")
    
    return {
        "id": attempt.id,
        "status": attempt.status,
        "total_marks": attempt.total_marks,
        "obtained_marks": attempt.obtained_marks,
        "percentage": attempt.percentage,
        "evaluation_type": attempt.evaluation_type,
        "evaluation": attempt.evaluation,
        "evaluated_at": attempt.evaluated_at.isoformat()
    }