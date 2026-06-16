from flask import g, jsonify

from services.auth.register_service import register_user
from validators.auth.register_schamas import (
    RegistrationRequest,
    RegistrationResponse
)
from decorators.json_required import json_required
from utils.response_envelopes import create_success_response

from . import auth_bp

# Register a user route
@auth_bp.post("/register")
@json_required
def register_endpoint():
    """
    Endpoint to register a new user.
    """
    payload = RegistrationRequest(**g.json_data)

    user = register_user(payload)

    return jsonify(
        create_success_response(
                RegistrationResponse(
                id = user.id,
                email = user.email,
                message = "User registered successfully"
            ).model_dump()
        )
    ), 201