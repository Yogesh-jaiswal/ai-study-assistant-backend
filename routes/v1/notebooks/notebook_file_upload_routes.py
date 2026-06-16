import logging
from uuid import UUID
from flask import g, jsonify, Blueprint

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
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response

# Set up logging
logger = logging.getLogger(__name__)

# Custom uploads blueprint for notebook file uploads
upload_bp = Blueprint("uploads", __name__, url_prefix="<uuid:notebook_id>/uploads")


# Upload a new file route
@upload_bp.post("")
@json_required
@login_required
def upload_file_endpoint(notebook_id: UUID):
    """
    Endpoint to upload a file to a notebook.
    Expects a JSON payload with the file details.
    """
    payload = FileUploadRequest(**g.json_data)

    upload_id = create_upload(str(notebook_id), g.user_id, payload)

    return jsonify(
        create_success_response(
            FileUploadedResponse(
                id=upload_id,
                message="file uploaded successfully"
            ).model_dump()
        )
    ), 201


# Retrieve all uploaded files from a notebook route
@upload_bp.get("")
@login_required
def get_all_uploads_endpoint(notebook_id: UUID):
    """
    Endpoint to retrieve all uploads for a notebook.
    """
    uploads = get_all_uploads(str(notebook_id), g.user_id)

    return jsonify(create_success_response(GetAllUploadsResponse(uploads=uploads).model_dump())), 200


# Retrieve a specific uploaded file route
@upload_bp.get("/<uuid:upload_id>")
@login_required
def get_upload_endpoint(notebook_id: UUID, upload_id: UUID):
    """
    Endpoint to retrieve a specific upload.
    """
    upload = get_upload(str(notebook_id), g.user_id, str(upload_id))

    return jsonify(create_success_response(GetUploadResponse(**upload).model_dump())), 200


# Delete a specific file upload route
@upload_bp.delete("/<uuid:upload_id>")
@login_required
def delete_upload_endpoint(notebook_id: UUID, upload_id: UUID):
    """
    Endpoint to delete a specific upload.
    """
    delete_upload(str(notebook_id), g.user_id, str(upload_id))

    return "", 204