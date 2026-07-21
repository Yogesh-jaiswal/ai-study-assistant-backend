from configs import get_settings
from services.ai.engine import AIEngine

from .mind_maps_prompt import create_mind_maps_prompt
from .mind_maps_schema import MindMapResponse


class MindMapGenerator:
    """Coordinates mind map generation using the AI engine."""

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, resources: str, generation_options: dict):

        prompt = create_mind_maps_prompt(resources)

        return self.engine.complete(prompt, MindMapResponse)