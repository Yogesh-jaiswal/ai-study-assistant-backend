from flask import g, jsonify, request

from services.auth.refresh_token_service import (
    create_refresh_token,
    verify_refresh_token,
    revoke_refresh_token
)
from services.auth.jwt_service import create_access_token
from validators.auth.login_schemas import LoginResponse
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from configs import settings

from . import auth_bp

# Re login the user and rotate refresh token
@auth_bp.get(
    "/refresh",
    summary="Re login the user and rotate refresh token",
    responses={
        200: LoginResponse,
        400: RequestJSONErrorResponse,
        401: UnauthorizedResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
def refresh_endpoint():
    """
    Endpoint to re login the user and rotate refresh token
    """
    refresh_token = request.cookies.get("refresh_token")

    session = verify_refresh_token(refresh_token)

    revoke_refresh_token(session)

    new_access_token = create_access_token(session.user_id)
    
    response = jsonify(
        LoginResponse(
            access_token = new_access_token,
            expires_in = settings.ACCESS_TOKEN_MINUTES * 60,
            message = "Re login successful"
        ).model_dump()
    )

    new_refresh_token = create_refresh_token(session.user_id)

    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Strict",
        max_age=30*24*60*60
    )

    return response, 200