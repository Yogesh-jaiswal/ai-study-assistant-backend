"""
Notebook AI-content API routes.

Provides endpoints for creating, retrieving, and interacting
with AI-generated content associated with notebooks.
"""

from flask import Blueprint
from .ai_content_attempt_routes import attempt_bp

# Blueprint for AI content routes
ai_content_bp = Blueprint("ai_contents", __name__, url_prefix="<uuid:notebook_id>/contents")

# Register the attempt blueprint with the AI content blueprint
from . import notebook_ai_content_routes

# Register the attempt blueprint with the AI content blueprint
ai_content_bp.register_blueprint(attempt_bp)