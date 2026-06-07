import logging

from app import create_app
from configs import settings
from validators.response_schemas import HealthResponse
from validators.error_response_schemas import (
    RateLimitExceededResponse,
    ServerErrorResponse
)

# Set up app logger
logger = logging.getLogger("app")

# Creating the app
app = create_app()

@app.get(
        "/",
        summary = "Health check endpoint to verify that the application is running",
        responses = {
            200: HealthResponse,
            429: RateLimitExceededResponse,
            500: ServerErrorResponse
        }
)
def home():
    """Health check endpoint to verify that the application is running."""
    logger.info("health check route called")
    return {
        "message": "AI Study Assistant is running"
    }

if __name__ == "__main__":
    app.run(debug=settings.DEBUG)