from typing import Any

def create_success_response(success_response: dict[str: Any]) -> dict[str, Any]:
    return {
        "success": True,
        "data": success_response,
        "error": None
    }

def create_error_envelope(error_response: dict[str: Any]) -> dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": error_response
    }