import logging
from pydantic import ValidationError
from typing import Any

from validators.request_schemas import QuizRequest

from services.ai.llm_client import generate_response
from validators.response_schemas import QuizResponse
from exceptions import ResponseValidationError

# Set up logging
logger = logging.getLogger(__name__)

def generate_quiz(payload: QuizRequest) -> dict[str: Any]:
    """Generates a quiz based on the provided payload."""

    logger.info("calling quiz generation service")

    ai_output = generate_response(payload, task="quiz") # Generate AI response based on the payload and task type

    # Validate the AI response against the QuizResponse schema
    try:
        validated_response = QuizResponse.model_validate(
            ai_output,
            context={"n": payload.n}
        )
    except ValidationError:
        logger.exception(f"response validation failed")

        raise ResponseValidationError(
            "model response failed"
        )
    
    logger.info("request completed successfully")

    return validated_response.model_dump()