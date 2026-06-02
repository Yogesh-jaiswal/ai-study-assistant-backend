import logging
from flask import g, jsonify
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel

from services.uploads.upload_services import (
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

# Set up logging
logger = logging.getLogger(__name__)

# Custom uploads blueprint for notebook file uploads
upload_bp = APIBlueprint("uploads", __name__, url_prefix="<int:notebook_id>/uploads")

# Path parameter schemas
class NotebookIDPathParams(BaseModel):
    notebook_id: int

class UploadIDPathParams(NotebookIDPathParams):
    upload_id: int

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
def upload_file_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to upload a file to a notebook.
    Expects a JSON payload with the file details.
    """
    payload = FileUploadRequest(**g.json_data)

    upload_id = create_upload(path.notebook_id, payload)

    return jsonify(
        FileUploadedResponse(
            id=upload_id,
            message="file uploaded successfully"
        ).model_dump()
    ), 201

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
def get_all_uploads_endpoint(path: NotebookIDPathParams):
    """
    Endpoint to retrieve all uploads for a notebook.
    """
    uploads = get_all_uploads(path.notebook_id)

    return jsonify(GetAllUploadsResponse(uploads=uploads).model_dump()), 200

@upload_bp.get(
    "/<int:upload_id>",
    summary = "Endpoint to retrieve a specific upload",
    responses = {
        200: GetUploadResponse,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
def get_upload_endpoint(path: UploadIDPathParams):
    """
    Endpoint to retrieve a specific upload.
    """
    upload = get_upload(path.notebook_id, path.upload_id)

    return jsonify(GetUploadResponse(**upload).model_dump()), 200

@upload_bp.delete(
    "/<int:upload_id>",
    summary = "Endpoint to delete a specific upload",
    responses = {
        204: None,
        404: ResourceNotFoundResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
def delete_upload_endpoint(path: UploadIDPathParams):
    """
    Endpoint to delete a specific upload.
    """
    delete_upload(path.notebook_id, path.upload_id)

    return "", 204