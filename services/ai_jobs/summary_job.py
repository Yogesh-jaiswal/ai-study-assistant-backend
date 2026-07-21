from .base_job import BaseJob
from services.summaries.summary_generator import SummaryGenerator
from services.ai_generation.generation_bundle import GenerationBundle

class SummaryGenerationJob(BaseJob):
    """Orchestrates summary generation task as a celery job"""
    def execute(self, generation_options: dict, bundle: GenerationBundle) -> dict:
        resources = bundle.to_prompt()
        
        generator = SummaryGenerator()
        
        response  = generator.generate(
            resources,
            generation_options
        )

        return response