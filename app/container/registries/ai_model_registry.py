from .base_registry import Registory

from providers.ai_providers.fake_provider import FakeAIProvider
from providers.ai_providers.gemini_provider import GeminiAIProvider

AI_MODEL_PROVIDERS = {
    "FAKE": FakeAIProvider,
    "GEMINI": GeminiAIProvider
}

ai_registry = Registory(AI_MODEL_PROVIDERS)