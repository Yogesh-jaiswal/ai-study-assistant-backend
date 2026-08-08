from .base_job import BaseJob
from services.mind_maps.mind_maps_generator import MindMapGenerator
from services.ai_generation.generation_bundle import GenerationBundle

class MindMapGenerationJob(BaseJob):
    """Orchestrates mind map generation task as a celery job."""
    def execute(self, generation_options: dict, bundle: GenerationBundle) -> dict:
        resources = bundle.to_prompt()

        generator = MindMapGenerator()
        
        response  = generator.generate(
            resources,
            generation_options
        )

        return response