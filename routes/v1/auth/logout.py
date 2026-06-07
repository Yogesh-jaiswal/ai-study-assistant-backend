from flask import g, jsonify, request

from services.auth.refresh_token_service import revoke_refresh_token, verify_refresh_token
from validators.auth.login_schemas import (
    LogoutResponse
)
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from decorators.login_required import login_required
from configs import settings

from . import auth_bp

# Logout a user route
@auth_bp.get(
    "/logout",
    summary="Logs out a user and revokes refresh token",
    responses={
        200: LogoutResponse,
        400: RequestJSONErrorResponse,
        401: UnauthorizedResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
def logout_endpoint():
    """
    Endpoint to logout the user and revoke refresh token
    """
    refresh_token = request.cookies.get("refresh_token")

    session = verify_refresh_token(refresh_token)

    revoke_refresh_token(session)

    response = jsonify(
        LogoutResponse(
            message = "Log out successful"
        ).model_dump()
    )

    response.delete_cookie("refresh_token")

    return response