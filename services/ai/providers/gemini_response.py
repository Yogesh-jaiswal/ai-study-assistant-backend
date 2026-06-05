import logging
import google.generativeai as genai

from configs.settings import settings
from exceptions import LLMError

# Set up logging
logger = logging.getLogger(__name__)

def create_gemini_response(prompt: str) -> str:
    """Creates a response from the Gemini model based on the given prompt."""

    API_KEY = settings.MODEL_API_KEY # Ensure that the API key is set in the settings
    MODEL = settings.MODEL_NAME # Ensure that the model name is set in the settings

    if not API_KEY:
        raise LLMError("GEMINI_API_KEY not set")

    if not MODEL:
        raise LLMError("MODEL_NAME not set")

    # Configure the Gemini API client with the provided API key    
    genai.configure(api_key=API_KEY) 

    model = genai.GenerativeModel(MODEL)

    # Generate content using the model and handle any exceptions that may occur
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        logger.error(f"model request failed: {e}")
        raise LLMError("model request failed")
    
    return response.text