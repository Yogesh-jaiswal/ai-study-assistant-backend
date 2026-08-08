import logging
from datetime import datetime

from redis.exceptions import ConnectionError, TimeoutError

from app.celery_app import celery_app as celery
from services.attempt_jobs.attempt_job_registry import ATTEMPT_JOB_REGISTRY
from models.enums import EvaluationTypes, ProcessingStatus
from repositories.user_attempt_repository import update_attempt, get_user_attempt_by_attempt_id
from services.attempts.attempt_context import AttemptContext
from services.attempts.attempt_loader import AttemptLoader
from exceptions import ResourceNotFoundError

# Set up logger
logger = logging.getLogger(__name__)

@celery.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def evaluate_user_attempt(
    self, 
    evaluation_type: EvaluationTypes, 
    attempt_id: str,
    content_id: str,
    notebook_id: str, 
    user_id: str,
    evaluation_context: dict
) -> dict:
    """
    Celery task to evaluate a user's attempt based on the specified evaluation type and context. 
    It retrieves the attempt, updates its status, executes the appropriate evaluation job, and updates the attempt with the results.
    """
    attempt = get_user_attempt_by_attempt_id(attempt_id, content_id, notebook_id, user_id)

    evaluation_context = AttemptContext(**evaluation_context)

    if not attempt:
        raise ResourceNotFoundError("Attempt not found!")
    
    attempt.status = ProcessingStatus.PROCESSING

    update_attempt(attempt)
    
    job = ATTEMPT_JOB_REGISTRY.get(evaluation_type)

    if not job:
        raise RuntimeError(f"No attempt job registered for {evaluation_type}")
    
    bundle = AttemptLoader.load(evaluation_context, notebook_id, user_id)
    
    try:
        evaluation = job.execute(bundle)
    except Exception:
        attempt.status = ProcessingStatus.FAILED
        update_attempt(attempt)

        logger.exception("Evaluation failed")
        raise RuntimeError("Evaluation failed")
    
    attempt.status = ProcessingStatus.COMPLETED
    attempt.total_marks = evaluation["total_marks"]
    attempt.obtained_marks = evaluation["obtained_marks"]
    attempt.percentage = evaluation["percentage"]
    attempt.evaluation = evaluation
    
    update_attempt(attempt)

    return {
        "attempt_id": attempt.id,
        "attempt_status": attempt.status
    }