from abc import ABC, abstractmethod

from services.attempts.attempt_bundle import EvaluationBundle

class BaseJob(ABC):
    @abstractmethod
    def execute(self, generation_options: dict, bundle: EvaluationBundle) -> dict:
        """Execute the ai job with given options."""
        pass