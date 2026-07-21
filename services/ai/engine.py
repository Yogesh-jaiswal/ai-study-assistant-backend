from typing import Any

from pydantic import BaseModel

from .models.fake_provider import FakeProvider
from .models.gemini_provider import GeminiProvider

class AIEngine:
    AI_PROVIDERS = {
        "FAKE": FakeProvider,
        "GEMINI": GeminiProvider
    }

    def __init__(self, provider):
        self.provider = provider

    def complete(self, prompt: str, response_schema: type[BaseModel], generation_options: dict | None = None) -> dict[str, Any]:
        model = self.AI_PROVIDERS.get(self.provider)

        if not model:
            raise ValueError("Invalid AI provider")
        
        return model().generate(prompt, response_schema, generation_options)