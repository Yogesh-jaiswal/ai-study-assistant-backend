"""
Authentication API routes.

Provides endpoints for user registration, login, logout,
token refresh, and retrieval of the authenticated user's
information.
"""

from flask import Blueprint

# Blueprint for auth-related routes
auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Load all the auth related routes
from . import register, login, me, refresh, logout