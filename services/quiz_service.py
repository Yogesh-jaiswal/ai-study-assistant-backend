import logging
from pydantic import ValidationError

from genai.llm_client import generate_response
from validators.response_schemas import QuizResponse
from exceptions import ResponseValidationError

# Set up logging
logger = logging.getLogger(__name__)

def generate_quiz(payload):
    """Generates a quiz based on the provided payload."""

    logger.info("calling quiz generation service")

    ai_output = generate_response(payload, task="quiz") # Generate AI response based on the payload and task type

    # Validate the AI response against the QuizResponse schema
    try:
        validated_response = QuizResponse.model_validate(
            ai_output,
            context={"n": payload.n}
        )
    except ValidationError as e:
        logger.error(f"response validation failed: {e}")

        raise ResponseValidationError(
            "model response failed"
        )
    
    logger.info("request completed successfully")

    return validated_response.model_dump()