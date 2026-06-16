from flask import g, jsonify, request

from services.auth.refresh_token_service import revoke_refresh_token, verify_refresh_token
from validators.auth.login_schemas import (
    LogoutResponse
)
from configs import get_settings
from utils.response_envelopes import create_success_response

from . import auth_bp

# Get the settings object
settings = get_settings()

# Logout a user route
@auth_bp.get("/logout")
def logout_endpoint():
    """
    Endpoint to logout the user and revoke refresh token
    """
    refresh_token = request.cookies.get("refresh_token")

    session = verify_refresh_token(refresh_token)

    revoke_refresh_token(session)

    response = jsonify(
        create_success_response(
            LogoutResponse(
                message = "Log out successful"
            ).model_dump()
        )
    )

    response.delete_cookie("refresh_token")

    return response