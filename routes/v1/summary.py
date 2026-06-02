import logging
from flask import g, jsonify
from flask_openapi3 import APIBlueprint

from services.legacy.summary_service import generate_summary
from validators.request_schemas import SummaryRequest
from validators.response_schemas import SummaryResponse
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from decorators.json_required import json_required
from configs.settings import settings
from app.extensions import limiter

# Blueprint for summary routes
summary_bp = APIBlueprint("summary", __name__)

# Set up logging
logger = logging.getLogger(__name__)

@summary_bp.post(
        "/summarize",
        summary = "Endpoint to summarize provided content",
        responses = {
            200: SummaryResponse,
            400: RequestJSONErrorResponse,
            422: ValidationErrorResponse,
            429: RateLimitExceededResponse,
            500: ServerErrorResponse
        }
)
@limiter.limit(settings.SUMMARY_RATE_LIMIT, override_defaults=False)
@json_required
def summarize():
    """Endpoint to summarize provided content."""
    payload  = SummaryRequest(**g.json_data)

    result = generate_summary(payload)

    return jsonify(result)