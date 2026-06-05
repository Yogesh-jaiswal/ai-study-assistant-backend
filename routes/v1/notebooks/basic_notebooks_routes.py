import logging
from flask import g, jsonify
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel

from services.notebooks.notebook_services import (
    create_notebook,
    delete_notebook,
    get_notebook,
    get_all_notebooks
)
from validators.notebook_schemas import (
    CreateNotebookRequest,
    NotebookCreatedResponse,
    GetNotebook,
    GetAllNotebooksResponse
)
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ResourceNotFoundResponse,
    ServerErrorResponse
)
from decorators.json_required import json_required
from decorators.login_required import login_required
from . import notebook_bp

# Set up logging
logger = logging.getLogger(__name__)

# Notebook path parameters model
class NotebookPath(BaseModel):
    id: int

# Create new notebook route
@notebook_bp.post(
    "",
    summary = "Endpoint to create a new notebook",
    responses = {
        201: NotebookCreatedResponse,
        400: RequestJSONErrorResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
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
        NotebookCreatedResponse(
            id=notebook_id,
            message="notebook created"
        ).model_dump()
    ), 201

# Get all notebooks route
@notebook_bp.get(
    "",
    summary = "Endpoint to retrieve all notebooks",
    responses = {
        200: GetAllNotebooksResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_all_notebooks_endpoint():
    """
    Endpoint to retrieve all notebooks.
    Expects a JSON payload with pagination and filtering options.
    """
    notebooks = get_all_notebooks(g.user_id)

    return jsonify(GetAllNotebooksResponse(data=notebooks).model_dump()), 200


# Retrieve specific notebook route
@notebook_bp.get(
    "/<int:id>",
    summary = "Endpoint to retrieve a specific notebook",
    responses = {
        200: GetNotebook,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_notebook_endpoint(path: NotebookPath):
    notebook = get_notebook(path.id, g.user_id)

    return jsonify(GetNotebook(**notebook).model_dump()), 200


# Notebook deletion route
@notebook_bp.delete(
    "/<int:id>",
    summary = "Endpoint to delete a specific notebook",
    responses = {
        204: None,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def delete_notebook_endpoint(path: NotebookPath):
    """
    Endpoint to delete a specific notebook.
    """
    delete_notebook(path.id, g.user_id)

    return "", 204