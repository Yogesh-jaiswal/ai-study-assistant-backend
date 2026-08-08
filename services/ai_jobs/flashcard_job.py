from .base_job import BaseJob
from services.flashcards.flashcard_generator import FlashcardGenerator
from services.ai_generation.generation_bundle import GenerationBundle

class FlashcardGenerationJob(BaseJob):
    """Orchestrates flashcard generation task as a celery job."""
    def execute(self, generation_options: dict, bundle: GenerationBundle) -> dict:
        resources = bundle.to_prompt()

        generator = FlashcardGenerator()
        
        response  = generator.generate(
            resources,
            generation_options
        )

        response["total_cards"] = generation_options["total_cards"]

        return response