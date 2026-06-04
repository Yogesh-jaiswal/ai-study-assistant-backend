from flask_openapi3 import APIBlueprint
from .summary import summary_bp
from .quiz import quiz_bp
from .notebooks import notebook_bp
from .auth import auth_bp

# Blueprint for version 1 of the API
v1_bp = APIBlueprint("v1", __name__, url_prefix="/v1")

# Register the blueprints with the v1 blueprint
v1_bp.register_api(summary_bp)
v1_bp.register_api(quiz_bp)
v1_bp.register_api(notebook_bp)
v1_bp.register_api(auth_bp)