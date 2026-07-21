from uuid import UUID
from flask import Blueprint, g, jsonify, request

from services.ai_generation.generation_service import (
    get_ai_content,
    get_all_ai_content,
    delete_ai_content
)
from validators.ai_content.basic_schemas import (
    GetAIContentResponse,
    GetAllAIContentsResponse
)
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response
from configs import get_settings
from . import ai_content_bp

# Retreive all ai contents from a notebook route
@ai_content_bp.get("")
@login_required
def get_all_ai_content_endpoint(notebook_id: UUID):
    """
    Endpoint to retrieve all ai contents from a notebook.
    """
    limit = request.args.get("limit", default=20, type=int)
    limit = min(limit, get_settings().MAX_LIMIT)

    page = request.args.get("page", default=1, type=int)
    offset = (page - 1) * limit

    ai_contents = get_all_ai_content(str(notebook_id), g.user_id, limit, offset)

    return jsonify(create_success_response(GetAllAIContentsResponse(ai_contents=ai_contents).model_dump()))


# Retreive a specific ai content route
@ai_content_bp.get("/<uuid:ai_content_id>")
@login_required
def get_ai_content_endpoint(notebook_id: UUID, ai_content_id: UUID):
    """
    Endpoint to retrieve a specific ai_content
    """
    ai_content = get_ai_content(str(notebook_id), g.user_id, str(ai_content_id))

    return jsonify(create_success_response(GetAIContentResponse(**ai_content).model_dump()))


# Delete a specific ai_content route
@ai_content_bp.delete("/<uuid:ai_content_id>")
@login_required
def delete_ai_content_endpoint(notebook_id: UUID, ai_content_id: UUID):
    """
    Endpoint to delete a specific ai_content.
    """

    delete_ai_content(str(notebook_id), g.user_id, str(ai_content_id))

    return "", 204