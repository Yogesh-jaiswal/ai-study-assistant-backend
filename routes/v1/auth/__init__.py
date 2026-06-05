from flask_openapi3 import APIBlueprint

# Blueprint for auth-related routes
auth_bp = APIBlueprint('auth', __name__, url_prefix="/auth")

from . import register
from . import login
from . import me