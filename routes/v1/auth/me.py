from flask import g, jsonify
from decorators.login_required import login_required
from services.auth.me_service import get_user
from validators.auth.me_schemas import GetMeResponse
from utils.response_envelopes import create_success_response
from . import auth_bp

@auth_bp.get("/me")
@login_required
def get_me():
    user = get_user(g.user_id)

    return jsonify(
        create_success_response(
            GetMeResponse(
                id=user.id,
                email=user.email,
                username=user.username
            ).model_dump()
        )
    )