from flask import Blueprint
from .notebook_file_upload_routes import upload_bp
from .ai_content import ai_content_bp

# Blueprint for notebook-related routes
notebook_bp = Blueprint('notebook', __name__, url_prefix='/notebooks')

# Loading basic notebook routes
from . import basic_notebooks_routes

# Loading chat route
from . import notebook_ask_routes

# Loading ai content creation routes
from .ai_content import notebook_ai_content_creation_routes

# Register the blueprints with the notebook blueprint
notebook_bp.register_blueprint(upload_bp)
notebook_bp.register_blueprint(ai_content_bp)