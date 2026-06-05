import logging
from pydantic import ValidationError
from typing import Any

from validators.request_schemas import SummaryRequest
from services.ai.llm_client import generate_response
from validators.response_schemas import SummaryResponse
from exceptions import ResponseValidationError

# Set up logging
logger = logging.getLogger(__name__)

def generate_summary(payload: SummaryRequest) -> dict[str, Any]:
    """Generates a summary based on the provided payload."""

    logger.info("calling summary generation service")

    ai_output = generate_response(payload, task="summary") # Generate the response using the LLM client

    # Validate the response against the SummaryResponse schema
    try:
        validated_response = SummaryResponse(**ai_output)
    except ValidationError:
        logger.exception(f"response validation failed")

        raise ResponseValidationError(
            "model response failed"
        )
    
    logger.info("request completed successfully")

    return validated_response.model_dump()