import logging
from functools import wraps
from flask import request, g

from exceptions import RequestJSONError

# Set up logging
logger = logging.getLogger(__name__)

def json_required(func):
    """Decorator to ensure that the request body contains valid JSON data."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_id = getattr(g, "request_id", "unknown")
        data = request.get_json(silent = True)

        if data is None:
            logger.error(f"[{request_id}] request rejected: body is not valid JSON")

            raise RequestJSONError(
                "Request body must contain valid JSON"
            )
        
        g.json_data = data

        return func(*args, **kwargs)
    return wrapper