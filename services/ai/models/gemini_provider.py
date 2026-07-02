from typing import Any
from functools import cache

from google import genai
from google.genai import Client
from pydantic import BaseModel

from configs import get_settings

@cache
def get_gemini_client(api_key: str) -> Client:
    """Create and cache a Gemini client."""
    return genai.Client(api_key=api_key)

class GeminiProvider:

    def __init__(self):
        self.client = get_gemini_client(get_settings().MODEL_API_KEY)

    def generate(self, prompt: str, response_schema: type[BaseModel]) -> dict[str, Any]:

        response = self.client.models.generate_content(
            model=get_settings().MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
                "system_instruction": "You are a study-focused tutor that responds in JSON format according to the provided schema."
            }
        )

        
        response.parsed.model_dump()