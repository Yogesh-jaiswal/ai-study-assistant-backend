from abc import ABC, abstractmethod

from services.ai_generation.generation_bundle import GenerationBundle

class BaseJob(ABC):
    @abstractmethod
    def execute(self, generation_options: dict, bundle: GenerationBundle) -> dict:
        """Execute the ai job with given options."""
        pass