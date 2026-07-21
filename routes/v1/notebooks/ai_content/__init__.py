from flask import Blueprint
from .ai_content_attempt_routes import attempt_bp

ai_content_bp = Blueprint("ai_contents", __name__, url_prefix="<uuid:notebook_id>/contents")

from . import notebook_ai_content_routes

ai_content_bp.register_blueprint(attempt_bp)