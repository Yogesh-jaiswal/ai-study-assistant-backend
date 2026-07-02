import logging
from functools import cache

from google import genai
from google.genai import Client

from configs import get_settings
from exceptions import LLMError

logger = logging.getLogger(__name__)


@cache
def get_gemini_client(api_key: str) -> Client:
    """Create and cache a Gemini client."""
    return genai.Client(api_key=api_key)


def create_gemini_response(prompt: str) -> str:
    """Generate a response using the configured Gemini model."""
    settings = get_settings()

    if not settings.MODEL_API_KEY:
        raise LLMError("MODEL_API_KEY not configured")

    if not settings.MODEL_NAME:
        raise LLMError("MODEL_NAME not configured")

    try:
        response = get_gemini_client(
            settings.MODEL_API_KEY
        ).models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt,
        )

        if not response.text:
            raise LLMError("Gemini returned an empty response")

        return response.text

    except LLMError:
        raise

    except Exception as exc:
        logger.exception("Gemini request failed")
        raise LLMError("Model request failed") from exc