from flask import g, jsonify

from services.auth.login_service import login_user
from validators.auth.login_schemas import (
    LoginRequest,
    LoginResponse
)
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from decorators.json_required import json_required
from configs.settings import settings

from . import auth_bp

# Login a user route
@auth_bp.post(
    "/login",
    summary="Logs in a user and generates an access token",
    responses={
        200: LoginResponse,
        400: RequestJSONErrorResponse,
        401: UnauthorizedResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@json_required
def login_endpoint():
    """
    Endpoint to Log in a user and generate an access token.
    """
    payload = LoginRequest(**g.json_data)

    token = login_user(payload)

    return jsonify(
        LoginResponse(
            access_token = token,
            expires_in = settings.ACCESS_TOKEN_MINUTES * 60,
            message = "Log in successful"
        ).model_dump()
    ), 200