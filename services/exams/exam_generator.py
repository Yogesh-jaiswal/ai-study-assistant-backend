from configs import get_settings
from services.ai.engine import AIEngine

from .exam_prompt import create_exam_prompt
from .exam_schema import ExamResponse


class ExamGenerator:
    """Coordinates exam generation using the AI engine."""

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, resources: str, generation_options):

        prompt = create_exam_prompt(resources, generation_options["difficulty"])

        response = self.engine.complete(prompt, ExamResponse, generation_options)
        
        return response