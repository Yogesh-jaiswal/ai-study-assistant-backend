from flask import g, jsonify

from services.legacy.summary_service import generate_summary
from validators.request_schemas import SummaryRequest
from decorators.json_required import json_required
from decorators.login_required import login_required
from configs import get_settings
from app.extensions import limiter
from utils.response_envelopes import create_success_response
from . import v1_bp

# Get the settings object
settings = get_settings()

@v1_bp.post("/summarize")
@limiter.limit(settings.SUMMARY_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def summarize():
    """Endpoint to summarize provided content."""
    payload  = SummaryRequest(**g.json_data)

    result = generate_summary(payload)

    return jsonify(create_success_response(result))