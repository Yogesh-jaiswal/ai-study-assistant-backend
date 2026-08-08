import os
from uuid import UUID
from flask import g, jsonify, Blueprint, request, send_file, current_app

from services.uploads.upload_service import (
    upload_file,
    get_all_uploads,
    get_upload,
    preview_file,
    delete_upload
)
from services.uploads.yt_uploads_service import upload_yt_video
from validators.upload_schemas import (
    FileUploadedResponse,
    GetAllUploadsResponse,
    GetUploadResponse,
    YoutubeUploadRequest
)
from exceptions import BadRequestError
from models.enums import UploadPurpose
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.response_envelopes import create_success_response
from configs import get_settings

# Custom uploads blueprint for notebook file uploads
upload_bp = Blueprint("uploads", __name__, url_prefix="<uuid:notebook_id>/uploads")


# Upload a new file route
@upload_bp.post("")
@login_required
def upload_file_endpoint(notebook_id: UUID):
    """
    Endpoint to upload a file to a notebook.
    """
    files = request.files.getlist("files")
    purpose = request.args.get("purpose", default="notes")

    try:
        upload_purpose = UploadPurpose(purpose)
    except ValueError:
        raise BadRequestError("Unknown upload purpose provided")

    if not files:
        raise BadRequestError("No file provided")
    
    uploads = []
    for file in files:
        uploads.append(upload_file(str(notebook_id), g.user_id, file, upload_purpose))

    return jsonify(
        create_success_response(
            [FileUploadedResponse(**upload).model_dump() for upload in uploads]
        )
    ), 201


# Retrieve all uploaded files from a notebook route
@upload_bp.get("")
@login_required
def get_all_uploads_endpoint(notebook_id: UUID):
    """
    Endpoint to retrieve all uploads for a notebook.
    """
    purpose = request.args.get("purpose", default="all")

    limit = request.args.get("limit", default=20, type=int)
    limit = min(limit, get_settings().MAX_LIMIT)

    page = request.args.get("page", default=1, type=int)
    offset = (page - 1) * limit

    try:
        upload_purpose = UploadPurpose(purpose) if purpose != "all" else None
    except ValueError:
        raise BadRequestError("Unknown upload purpose provided")
    
    uploads = get_all_uploads(str(notebook_id), g.user_id, upload_purpose, limit, offset)

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

# Preview a specific uploaded file route
@upload_bp.get("/<uuid:upload_id>/preview")
@login_required
def preview_upload_endpoint(notebook_id: UUID, upload_id: UUID):
    """
    Endpoint to preview a specific upload.
    """
    file_path = preview_file(str(notebook_id), g.user_id, str(upload_id))

    return send_file(
        file_path, 
        as_attachment=False
    ), 200

# Delete a specific file upload route
@upload_bp.delete("/<uuid:upload_id>")
@login_required
def delete_upload_endpoint(notebook_id: UUID, upload_id: UUID):
    """
    Endpoint to delete a specific upload.
    """
    delete_upload(str(notebook_id), g.user_id, str(upload_id))

    return "", 204

# Upload a new youtube video
@upload_bp.post("/youtube")
@json_required
@login_required
def upload_yt_video_endpoint(notebook_id: UUID):
    """
    Endpoint to upload a youtube video to a notebook.
    """
    payload = YoutubeUploadRequest(**g.json_data)
    
    upload = upload_yt_video(str(notebook_id), g.user_id, payload)

    return jsonify(
        create_success_response(
            FileUploadedResponse(**upload).model_dump()
        )
    ), 201