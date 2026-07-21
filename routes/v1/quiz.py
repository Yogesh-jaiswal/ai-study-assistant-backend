from flask import g, jsonify

from services.legacy.quiz_service import generate_quiz
from validators.request_schemas import QuizRequest
from decorators.json_required import json_required
from decorators.login_required import login_required
from configs import get_settings
from app.extensions import limiter
from utils.response_envelopes import create_success_response
from . import v1_bp

# Get the settings object
settings = get_settings()

@v1_bp.post("/quiz")
@limiter.limit(settings.QUIZ_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def quiz():
    """Endpoint to generate a quiz based on provided content."""
    payload = QuizRequest(**g.json_data)
    
    result = generate_quiz(payload)

    return jsonify(create_success_response(result))