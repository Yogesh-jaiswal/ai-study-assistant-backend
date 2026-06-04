from flask_openapi3 import APIBlueprint

# Blueprint for auth-related routes
auth_bp = APIBlueprint('auth', __name__)

from . import register
from . import login