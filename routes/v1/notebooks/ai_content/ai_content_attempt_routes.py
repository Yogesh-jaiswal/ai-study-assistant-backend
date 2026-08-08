from uuid import UUID
from flask import Blueprint, g, jsonify, request

from services.attempts.attempt_services import (
    create_attempt,
    get_attempt,
    get_all_attempts
)
from validators.ai_content.evaluation_schemas import (
    EvaluateAttemptResponse,
    GetAllAttemptResponse,
    GetAttemptResponse,
    EvaluationRequest
)
from services.attempts.attempt_context import AttemptContext
from decorators.login_required import login_required
from decorators.json_required import json_required
from utils.response_envelopes import create_success_response
from configs import get_settings

# Custom attempt blueprint for notebook ai content attempts
attempt_bp = Blueprint("attempts", __name__, url_prefix="<uuid:content_id>/attempts")

# Create an attempt for the ai content route
@attempt_bp.post("")
@json_required
@login_required
def create_attempt_endpoint(notebook_id: UUID, content_id: UUID):
    """
    Endpoint to create an attempt for an ai content.
    """
    payload = EvaluationRequest(**g.json_data)

    context = AttemptContext(
        content_id=str(content_id),
        answers=payload.model_dump()["answers"]
    )

    response = create_attempt(str(notebook_id), g.user_id, context)

    return jsonify(
        create_success_response(
            EvaluateAttemptResponse(
                task_id=response["task_id"],
                attempt_id=response["attempt_id"],
                message="User attempt evaluation started"
            ).model_dump()
        )
    ), 202

# Retreive all attempt for an ai content route
@attempt_bp.get("")
@login_required
def get_all_attempts_endpoint(notebook_id: UUID, content_id: UUID):
    """
    Endpoint to retrieve all attempts for an ai content.
    """
    limit = request.args.get("limit", default=20, type=int)
    limit = min(limit, get_settings().MAX_LIMIT)

    page = request.args.get("page", default=1, type=int)
    offset = (page - 1) * limit

    attempts = get_all_attempts(str(content_id), str(notebook_id), g.user_id, limit, offset)

    return jsonify(create_success_response(GetAllAttemptResponse(attempts=attempts).model_dump()))


# Retreive a specific attempt route
@attempt_bp.get("/<uuid:attempt_id>")
@login_required
def get_attempt_endpoint(notebook_id: UUID, content_id: UUID, attempt_id: UUID):
    """
    Endpoint to retrieve a specific attempt
    """
    attempt = get_attempt(str(attempt_id), str(content_id), str(notebook_id), g.user_id)

    return jsonify(create_success_response(GetAttemptResponse(**attempt).model_dump()))