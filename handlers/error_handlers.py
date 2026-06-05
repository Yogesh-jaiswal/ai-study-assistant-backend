import logging
from typing import Any
from flask import jsonify, Response
from pydantic import ValidationError
from flask_limiter.errors import RateLimitExceeded
from flask_openapi3 import OpenAPI

from exceptions import (
    DatabaseError,
    LLMError,
    ResponseValidationError,
    RequestJSONError,
    ResourceNotFoundError,
    AuthenticationError
)

# Set up logging
logger = logging.getLogger(__name__)

# Helper function to create a consistent error response
def create_error_msg(error_type: str, message: str, status_code: int) -> Response:
    return jsonify({
            "error": {
                "type": error_type,
                "message": message
            }
        }), status_code

# Function to reconstruct validation errors into a more user-friendly format
def reconstruct_validation_errors(errors: dict) -> list[dict[str, Any]]:
    error_list = []
    for error in errors:
        current_level = {}

        current_level["field"] = error['loc'][-1]
        current_level["message"] = error['msg']

        error_list.append(current_level)

    return error_list

# Function to register all error handlers with the Flask app
def register_error_handlers(app: OpenAPI):
    @app.errorhandler(ValidationError)
    def handle_validation_errors(e):
        """Handle Pydantic validation errors and return a structured error response."""
        return create_error_msg(
            "validation_error",
            reconstruct_validation_errors(e.errors()),
            422
        )
    
    @app.errorhandler(LLMError)
    def handle_llm_errors(e):
        """Handle LLM-related errors and return a structured error response."""
        return create_error_msg(
            "llm_error",
            str(e),
            500
        )
    
    @app.errorhandler(ResponseValidationError)
    def handle_response_validation_errors(e):
        """Handle response validation errors and return a structured error response."""
        return create_error_msg(
            "response_validation_error",
            str(e),
            500
        )
    
    @app.errorhandler(RequestJSONError)
    def handle_json_errors(e):
        """Handle JSON parsing errors and return a structured error response."""
        return create_error_msg(
            "validation_error",
            str(e),
            400
        )
    
    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found_errors(e):
        """Handle resource not found errors and return a structured error response."""
        logger.warning(str(e)) # Log the resource not found error for monitoring purposes
        return create_error_msg(
            "resource_not_found",
            "Requested resource not found",
            404
        )
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_errors(e):
        """Handle rate limit errors and return a structured error response."""
        logger.warning(f"rate limit exceeded: {e.description}") # Log the rate limit error for monitoring purposes

        return create_error_msg(
            "rate_limit_error",
            "Too many requests",
            429
        )
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_errors(e):
        """Handle authentication errors and return a structured error response."""
        return create_error_msg(
            "authentication_error",
            str(e),
            401
        )

    @app.errorhandler(DatabaseError)
    def handle_database_errors(e):
        """Handle database errors and return a structured error response."""

        return create_error_msg(
            "database_error",
            "A database error occurred",
            500
        )
    
    """
    @app.errorhandler(Exception)
    def handle_unexpected_errors(e):
        logger.error(f"Unexpected error: {str(e)}", exc_info=True) # Log the unexpected error with stack trace for debugging purposes
        return create_error_msg(
            "internal_server_error",
            "unexpected server error",
            500
        )
    """