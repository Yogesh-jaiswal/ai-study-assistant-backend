import logging
from uuid import UUID
from flask import Blueprint, g, jsonify

from validators.query_schemas import(
    QueryRequest,
    QueryResponse
)
from . import notebook_bp
from services.chat.chat_services import answer_query
from app.extensions import limiter
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response
from configs import get_settings

# Get the settings object
settings = get_settings()

# Set up logging
logger = logging.getLogger(__name__)

# Chat route
@notebook_bp.post("<uuid:notebook_id>/ask")
@limiter.limit(settings.ASK_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def answer_query_endpoint(notebook_id: UUID):
    """
    Endpoint to answer a query from notebook uploads.
    Expects a JSON payload
    """
    payload = QueryRequest(**g.json_data)

    response = answer_query(str(notebook_id), g.user_id, payload)

    return jsonify(
        create_success_response(
            QueryResponse(
                **response
            ).model_dump()
        )
    ), 200