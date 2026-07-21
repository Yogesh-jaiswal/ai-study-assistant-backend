from flask import Blueprint
from .notebooks import notebook_bp
from .auth import auth_bp
from .blueprint_routes import blueprints_bp

# Blueprint for version 1 of the API
v1_bp = Blueprint("v1", __name__, url_prefix="/v1")

# Loading legacy routes and task status route
from . import summary, quiz, task_status

# Register the blueprints with the v1 blueprint
v1_bp.register_blueprint(notebook_bp)
v1_bp.register_blueprint(auth_bp)
v1_bp.register_blueprint(blueprints_bp)