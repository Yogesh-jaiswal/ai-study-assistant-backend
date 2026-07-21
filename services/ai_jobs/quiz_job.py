from uuid import uuid4

from .base_job import BaseJob
from services.quizzes.quiz_generator import QuizGenerator
from services.ai_generation.generation_bundle import GenerationBundle

class QuizGenerationJob(BaseJob):
    """Orchestrates quiz generation task as a celery job"""
    def execute(self, generation_options: dict, bundle: GenerationBundle) -> dict:
        resources = bundle.to_prompt()

        generator = QuizGenerator()
        
        response  = generator.generate(
            resources,
            generation_options
        )

        response["marks_per_question"] = generation_options["marks"]
        response["negative_marking"] = generation_options["negative_marking"]
        response["difficulty"] = generation_options["difficulty"]

        for question in response["questions"]:
            question["question_id"] = str(uuid4())

        return response