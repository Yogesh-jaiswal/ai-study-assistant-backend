import logging
from flask import g, jsonify
from flask_openapi3 import APIBlueprint

from services.legacy.quiz_service import generate_quiz
from validators.request_schemas import QuizRequest
from validators.response_schemas import QuizResponse
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from decorators.json_required import json_required
from configs.settings import settings
from app.extensions import limiter

# Blueprint for quiz routes
quiz_bp = APIBlueprint("quiz", __name__)

# Set up logging
logger = logging.getLogger(__name__)

@quiz_bp.post(
        "/quiz",
        summary = "Endpoint to generate a quiz based on provided content",
        responses = {
            200: QuizResponse,
            400: RequestJSONErrorResponse,
            422: ValidationErrorResponse,
            429: RateLimitExceededResponse,
            500: ServerErrorResponse
        }
)
@limiter.limit(settings.QUIZ_RATE_LIMIT, override_defaults=False)
@json_required
def quiz():
    """Endpoint to generate a quiz based on provided content."""
    payload = QuizRequest(**g.json_data)
    
    result = generate_quiz(payload)

    return jsonify(result)