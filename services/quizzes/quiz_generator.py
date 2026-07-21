from configs import get_settings
from services.ai.engine import AIEngine

from exceptions import AIResponseValidationError

from .quiz_prompt import create_quiz_prompt
from .quiz_schema import QuizResponse


class QuizGenerator:
    """Coordinates quiz generation using the AI engine."""

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, resources: str, generation_options):

        prompt = create_quiz_prompt(resources, generation_options["question_count"], generation_options["difficulty"])

        response = self.engine.complete(prompt, QuizResponse, generation_options)
    
        # Provider-native structured generation does not guarantee collection length, so the count is verified explicitly.
        if len(response["questions"]) != generation_options["question_count"]:
            raise AIResponseValidationError(
                "Generated quiz contains incorrect number of questions."
            )
        
        return response