from flask import Blueprint, g, jsonify, request

from services.blueprints.blueprint_services import (
    get_blueprint_by_slug,
    list_user_blueprints,
    list_public_blueprints,
    delete_blueprint,
    copy_blueprint,
    edit_blueprint,
    create_blueprint
)
from validators.blueprint_schemas import (
    GetBlueprintResponse,
    BlueprintCreationResponse,
    ListBlueprintResponse,
    BlueprintCreationRequest
)
from decorators.login_required import login_required
from decorators.json_required import json_required
from utils.response_envelopes import create_success_response
from configs import get_settings
from exceptions import BadRequestError

# Custom ai content blueprint for notebook ai contents
blueprints_bp = Blueprint("blueprints", __name__, url_prefix="blueprints")

# Create a new blueprint route
@blueprints_bp.post("")
@json_required
@login_required
def create_blueprint_endpoint():
    """
    Endpoint to create a new blueprint.
    """
    payload = BlueprintCreationRequest(**g.json_data)

    blueprint_slug = create_blueprint(g.user_id, payload)

    return jsonify(
        create_success_response(
            BlueprintCreationResponse(
                blueprint_slug=blueprint_slug,
                message="Blueprint created successfully"
            ).model_dump()
        )
    ), 201

# Retrieve all user or public blueprints route
@blueprints_bp.get("")
@blueprints_bp.get("/me")
@login_required
def list_blueprints_endpoint():
    """
    Endpoint to retrieve all public or user blueprints.
    """
    keyword = request.args.get("keyword")

    limit = request.args.get("limit", default=20, type=int)
    limit = min(limit, get_settings().MAX_LIMIT)

    page = request.args.get("page", default=1, type=int)
    offset = (page - 1) * limit

    if (limit <= 0 or page <= 0):
        raise BadRequestError("limit and page must be greater than 0")
    
    if request.path.endswith("me"):
        blueprints = list_user_blueprints(g.user_id, keyword, limit, offset)
    else:
        blueprints = list_public_blueprints(keyword, limit, offset)

    return jsonify(create_success_response(ListBlueprintResponse(blueprints=blueprints).model_dump()))

# Retrieve a specific blueprint by slug route
@blueprints_bp.get("/<string:slug>")
@login_required
def get_blueprint_endpoint(slug: str):
    """
    Endpoint to retrieve a specific blueprint by slug.
    """
    blueprint = get_blueprint_by_slug(slug, g.user_id)

    return jsonify(create_success_response(GetBlueprintResponse(**blueprint).model_dump()))

# Save a public blueprint in user's own collection route
@blueprints_bp.post("<string:slug>/save")
@login_required
def save_blueprint_endpoint(slug: str):
    """
    Endpoint to save a public blueprint.
    """
    blueprint_slug = copy_blueprint(slug, g.user_id)

    return jsonify(
        create_success_response(
            BlueprintCreationResponse(
                blueprint_slug=blueprint_slug,
                message="Blueprint saved successfully"
            ).model_dump()
        )
    )

# Edit a specific blueprint route
@blueprints_bp.patch("/<string:slug>")
@json_required
@login_required
def edit_blueprint_endpoint(slug: str):
    """
    Endpoint to edit a specific blueprint.
    """
    payload = BlueprintCreationRequest(**g.json_data)

    blueprint_slug = edit_blueprint(slug, g.user_id, payload)

    return jsonify(
        create_success_response(
            BlueprintCreationResponse(
                blueprint_slug=blueprint_slug,
                message="Blueprint edited successfully"
            ).model_dump()
        )
    )

# Delete a specific blueprint route
@blueprints_bp.delete("/<string:slug>")
@login_required
def delete_blueprint_endpoint(slug: str):
    """
    Endpoint to delete a specific blueprint.
    """

    delete_blueprint(slug, g.user_id)

    return "", 204