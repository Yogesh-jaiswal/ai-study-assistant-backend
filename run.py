import logging

from app.factory import create_app
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
    if settings.EMBEDDINGS_MODEL == "all-MiniLM-L6-v2":
        logger.warning(
            "English-only embeddings configured. "
            "Multilingual documents are supported but retrieval quality "
            "may be lower. Consider switching to a multilingual model "
            "if multilingual search is required."
            "\n You can change it by changing the app settings."
        )
    app.run(debug=settings.DEBUG)