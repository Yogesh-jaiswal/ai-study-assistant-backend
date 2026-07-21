from configs import get_settings
from services.ai.engine import AIEngine

from exceptions import AIResponseValidationError

from .flashcard_prompt import create_flashcard_prompt
from .flashcard_schema import FlashcardResponse


class FlashcardGenerator:
    """Coordinates flashcard generation using the AI engine."""

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, resources: str, generation_options):

        prompt = create_flashcard_prompt(resources, generation_options["total_cards"])

        response = self.engine.complete(prompt, FlashcardResponse, generation_options)

        # Provider-native structured generation does not guarantee collection length, so the count is verified explicitly.
        if len(response["flashcards"]) != generation_options["total_cards"]:
            raise AIResponseValidationError(
                "Generated flashcards contains incorrect number of cards."
            )
        
        return response