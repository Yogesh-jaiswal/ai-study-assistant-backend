from flask import g, jsonify
from decorators.login_required import login_required
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from services.auth.me_service import get_user
from validators.auth.me_schemas import GetMeResponse
from . import auth_bp

@auth_bp.get(
    "/me",
    summary="Returns the user's data",
    responses={
        200: GetMeResponse,
        400: RequestJSONErrorResponse,
        401: UnauthorizedResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@login_required
def get_me():
    user = get_user(g.user_id)

    return jsonify(
        GetMeResponse(
            id=user.id,
            email=user.email,
            username=user.username
        ).model_dump()
    )