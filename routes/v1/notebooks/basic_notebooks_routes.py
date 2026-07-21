from uuid import UUID
from flask import g, jsonify, request

from services.notebooks.notebook_service import (
    create_notebook,
    delete_notebook,
    get_notebook,
    get_all_notebooks,
    edit_notebook
)
from validators.notebook_schemas import (
    CreateNotebookRequest,
    NotebookCreatedResponse,
    GetNotebook,
    GetAllNotebooksResponse
)
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response
from configs import get_settings
from . import notebook_bp

# Create new notebook route
@notebook_bp.post("")
@json_required
@login_required
def create_notebook_endpoint():
    """
    Endpoint to create a new notebook.
    Expects a JSON payload with the notebook details.
    """
    payload = CreateNotebookRequest(**g.json_data)

    notebook_id = create_notebook(g.user_id, payload)

    return jsonify(
        create_success_response(
            NotebookCreatedResponse(
                id=notebook_id,
                message="notebook created"
            ).model_dump()
        )
    ), 201

# Get all notebooks route
@notebook_bp.get("")
@login_required
def get_all_notebooks_endpoint():
    """
    Endpoint to retrieve all notebooks.
    Expects a JSON payload with pagination and filtering options.
    """
    limit = request.args.get("limit", default=20, type=int)
    limit = min(limit, get_settings().MAX_LIMIT)

    page = request.args.get("page", default=1, type=int)
    offset = (page - 1) * limit

    notebooks = get_all_notebooks(g.user_id, limit, offset)

    return jsonify(create_success_response(GetAllNotebooksResponse(notebooks=notebooks).model_dump())), 200


# Retrieve specific notebook route
@notebook_bp.get("/<uuid:id>")
@login_required
def get_notebook_endpoint(id: UUID):
    notebook = get_notebook(str(id), g.user_id)

    return jsonify(create_success_response(GetNotebook(**notebook).model_dump())), 200


# Notebook edit route
@notebook_bp.patch("/<uuid:id>/edit")
@login_required
def edit_notebook_endpoint(id: UUID):
    """
    Endpoint to edit a specific notebook.
    Expects a JSON payload with pagination and filtering options.
    """
    payload = CreateNotebookRequest(**g.json_data)

    notebook_id = edit_notebook(str(id), g.user_id, payload)

    return jsonify(
        create_success_response(
            NotebookCreatedResponse(
                id=notebook_id,
                message="notebook created"
            ).model_dump()
        )
    ), 200


# Notebook deletion route
@notebook_bp.delete("/<uuid:id>")
@login_required
def delete_notebook_endpoint(id: UUID):
    """
    Endpoint to delete a specific notebook.
    """
    delete_notebook(str(id), g.user_id)

    return "", 204