from configs import get_settings
from services.ai.engine import AIEngine

from .summary_prompt import create_summary_prompt
from .summary_schema import SummaryResponse


class SummaryGenerator:
    """Coordinates summary generation using the AI engine."""

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, resources: str, generation_options: dict):

        prompt = create_summary_prompt(resources)

        return self.engine.complete(prompt, SummaryResponse)