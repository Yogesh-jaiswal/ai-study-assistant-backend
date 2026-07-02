from configs import get_settings
from services.ai.engine import AIEngine

from .summary_prompt import create_summary_prompt
from .summary_schema import SummaryResponse


class SummaryGenerator:

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, topic: str, notes: str):

        prompt = create_summary_prompt(topic, notes)

        return self.engine.complete(prompt, SummaryResponse)