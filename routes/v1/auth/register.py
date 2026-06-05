from flask import g, jsonify

from services.auth.register_service import register_user
from validators.auth.register_schamas import (
    RegistrationRequest,
    RegistrationResponse
)
from validators.error_response_schemas import (
    RequestJSONErrorResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
    RateLimitExceededResponse,
    ServerErrorResponse
)
from decorators.json_required import json_required

from . import auth_bp

# Register a user route
@auth_bp.post(
    "/register",
    summary="Register a new user",
    responses={
        201: RegistrationResponse,
        400: RequestJSONErrorResponse,
        401: UnauthorizedResponse,
        422: ValidationErrorResponse,
        429: RateLimitExceededResponse,
        500: ServerErrorResponse
    }
)
@json_required
def register_endpoint():
    """
    Endpoint to register a new user.
    """
    payload = RegistrationRequest(**g.json_data)

    user = register_user(payload)

    return jsonify(
        RegistrationResponse(
            id = user.id,
            email = user.email,
            message = "User registered successfully"
        ).model_dump()
    ), 201