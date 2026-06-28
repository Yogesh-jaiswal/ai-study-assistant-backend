import logging

from app import create_app
from configs import get_settings

# Get the settings object
settings = get_settings()

# Set up app logger
logger = logging.getLogger("app")

# Creating the app
app = create_app()

@app.get("/")
def home():
    """Health check endpoint to verify that the application is running."""
    logger.info("health check route called")
    return {
        "message": "AI Study Assistant is running"
    }

if __name__ == "__main__":
    app.run(debug=settings.DEBUG)