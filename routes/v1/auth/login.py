from flask import g, jsonify

from services.auth.login_service import login_user
from services.auth.refresh_token_service import create_refresh_token
from services.auth.jwt_service import create_access_token
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
from configs import settings

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

    user = login_user(payload)

    access_token = create_access_token(user.id)

    response = jsonify(
        LoginResponse(
            access_token = access_token,
            expires_in = settings.ACCESS_TOKEN_MINUTES * 60,
            message = "Log in successful"
        ).model_dump()
    )

    refresh_token = create_refresh_token(user.id)

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Strict",
        max_age=30*24*60*60
    )

    return response, 200