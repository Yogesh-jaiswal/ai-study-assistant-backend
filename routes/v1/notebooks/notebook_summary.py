import logging
from uuid import UUID
from flask import Blueprint, g, jsonify

from services.summaries.summary_service import (
    enqueue_summary_generation,
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
from app.extensions import limiter
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response
from configs import get_settings

# Get the settings object
settings = get_settings()

# Set up logging
logger = logging.getLogger(__name__)

# Custom summaries blueprint for notebook summaries
summary_bp = Blueprint("summaries", __name__, url_prefix="<uuid:notebook_id>/summaries")

# Generate a new summary route
@summary_bp.post("")
@limiter.limit(settings.SUMMARY_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_summary_endpoint(notebook_id: UUID):
    """
    Endpoint to generate a summary based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateSummaryRequest(**g.json_data)

    task_id = enqueue_summary_generation(str(notebook_id), g.user_id, payload)

    return jsonify(
        create_success_response(
            GenerateSummaryResponse(
                task_id=task_id,
                message="Summary generation started"
            ).model_dump()
        )
    ), 202

# Retreive all summaries from a notebook route
@summary_bp.get("")
@login_required
def get_all_summaries_endpoint(notebook_id: UUID):
    """
    Endpoint to retrieve all summaries from a notebook.
    """
    summaries = get_all_summaries(str(notebook_id), g.user_id)

    return jsonify(create_success_response(GetAllSummariesResponse(summaries=summaries).model_dump()))


# Retreive a specific summary route
@summary_bp.get("/<uuid:summary_id>")
@login_required
def get_summary_endpoint(notebook_id: UUID, summary_id: UUID):
    """
    Endpoint to retrieve a specific summary
    """
    summary = get_summary(str(notebook_id), g.user_id, str(summary_id))

    return jsonify(create_success_response(GetSummaryResponse(**summary).model_dump()))


# Delete a summary route
@summary_bp.delete("/<uuid:summary_id>")
@login_required
def delete_summary_endpoint(notebook_id: UUID, summary_id: UUID):
    """
    Endpoint to delete a specific summary.
    """

    delete_summary(str(notebook_id), g.user_id, str(summary_id))

    return "", 204