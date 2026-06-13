import logging
from uuid import UUID
from flask import g, jsonify
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel

from services.uploads.upload_service import (
    create_upload,
    get_all_uploads,
    get_upload,
    delete_upload
)
from validators.upload_schemas import (
    FileUploadRequest,
    FileUploadedResponse,
    GetAllUploadsResponse,
    GetUploadResponse
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

# Set up logging
logger = logging.getLogger(__name__)

# Custom uploads blueprint for notebook file uploads
upload_bp = APIBlueprint("uploads", __name__, url_prefix="<string:notebook_id>/uploads")

# Path parameter schemas
class NotebookIDPathParams(BaseModel):
    notebook_id: UUID

class UploadIDPathParams(NotebookIDPathParams):
    upload_id: UUID


# Upload a new file route
@upload_bp.post(
    "",
    summary = "Endpoint to upload a file to a notebook",
    responses = {
        201: FileUploadedResponse,
        400: RequestJSONErrorResponse,
        404: ResourceNotFoundResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@json_required
@login_required
def upload_file_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to upload a file to a notebook.
    Expects a JSON payload with the file details.
    """
    payload = FileUploadRequest(**g.json_data)

    upload_id = create_upload(str(path.notebook_id), g.user_id, payload)

    return jsonify(
        FileUploadedResponse(
            id=upload_id,
            message="file uploaded successfully"
        ).model_dump()
    ), 201


# Retrieve all uploaded files from a notebook route
@upload_bp.get(
    "",
    summary = "Endpoint to retrieve all uploads for a notebook",
    responses = {
        200: GetAllUploadsResponse,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_all_uploads_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to retrieve all uploads for a notebook.
    """
    uploads = get_all_uploads(str(path.notebook_id), g.user_id)

    return jsonify(GetAllUploadsResponse(uploads=uploads).model_dump()), 200


# Retrieve a specific uploaded file route
@upload_bp.get(
    "/<string:upload_id>",
    summary = "Endpoint to retrieve a specific upload",
    responses = {
        200: GetUploadResponse,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_upload_endpoint(path: UploadIDPathParams):
    """
    Endpoint to retrieve a specific upload.
    """
    upload = get_upload(str(path.notebook_id), g.user_id, str(path.upload_id))

    return jsonify(GetUploadResponse(**upload).model_dump()), 200


# Delete a specific file upload route
@upload_bp.delete(
    "/<string:upload_id>",
    summary = "Endpoint to delete a specific upload",
    responses = {
        204: None,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def delete_upload_endpoint(path: UploadIDPathParams):
    """
    Endpoint to delete a specific upload.
    """
    delete_upload(str(path.notebook_id), g.user_id, str(path.upload_id))

    return "", 204