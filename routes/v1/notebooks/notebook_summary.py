import logging
from uuid import UUID
from flask import g, jsonify
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel

from services.summaries.summary_services import (
    generate_summary,
    get_all_summaries,
    get_summary,
    delete_summary
)
from validators.summary_schemas import (
    GenerateSummaryRequest,
    GenerateSummaryResponse,
    GetAllSummariesResponse,
    GetSummaryResponse
)
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ResourceNotFoundResponse,
    ServerErrorResponse
)
from app.extensions import limiter
from decorators.json_required import json_required
from decorators.login_required import login_required
from configs import get_settings

# Get the settings object
settings = get_settings()

# Set up logging
logger = logging.getLogger(__name__)

# Custom summaries blueprint for notebook summaries
summary_bp = APIBlueprint("summaries", __name__, url_prefix="<string:notebook_id>/summaries")

# Path parameter schemas
class NotebookIDPathParams(BaseModel):
    notebook_id: UUID

class SummaryIDPathParams(NotebookIDPathParams):
    summary_id: UUID

# Generate a new summary route
@summary_bp.post(
    "",
    summary = "Endpoint to generate a based on selected uploads from a notebook",
    responses = {
        201: GenerateSummaryResponse,
        400: RequestJSONErrorResponse,
        404: ResourceNotFoundResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@limiter.limit(settings.SUMMARY_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_summary_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to generate a based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateSummaryRequest(**g.json_data)

    summary_id = generate_summary(str(path.notebook_id), g.user_id, payload)

    return jsonify(
        GenerateSummaryResponse(
            id=summary_id,
            message="summary generated successfully"
        ).model_dump()
    ), 201

# Retreive all summaries from a notebook route
@summary_bp.get(
    "",
    summary = "Endpoint to retrieve all summaries from a notebook",
    responses = {
        200: GetAllSummariesResponse,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_all_summaries_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to retrieve all summaries from a notebook.
    """
    summaries = get_all_summaries(str(path.notebook_id), g.user_id)

    return jsonify(GetAllSummariesResponse(summaries=summaries).model_dump())


# Retreive a specific summary route
@summary_bp.get(
    "/<string:summary_id>",
    summary = "Endpoint to retreive a specific summary",
    responses = {
        200: GetSummaryResponse,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_summary_endpoint(path: SummaryIDPathParams):
    """
    Endpoint to retrieve a specific summary
    """
    summary = get_summary(str(path.notebook_id), g.user_id, str(path.summary_id))

    return jsonify(GetSummaryResponse(**summary).model_dump())


# Delete a summary route
@summary_bp.delete(
    "/<string:summary_id>",
    summary = "Endpoint to delete a specific summary",
    responses = {
        204: None,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def delete_summary_endpoint(path: SummaryIDPathParams):
    """
    Endpoint to delete a specific summary.
    """

    delete_summary(str(path.notebook_id), g.user_id, str(path.summary_id))

    return "", 204