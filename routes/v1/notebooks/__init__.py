from flask_openapi3 import APIBlueprint
from .basic_notebooks_routes import base_bp
from .notebook_file_upload_routes import upload_bp
from .notebook_summary import summary_bp

# Blueprint for notebook-related routes
notebook_bp = APIBlueprint('notebook', __name__, url_prefix='/notebooks')

# Register the blueprints with the notebook blueprint
notebook_bp.register_blueprint(base_bp)
notebook_bp.register_blueprint(upload_bp)
notebook_bp.register_blueprint(summary_bp)