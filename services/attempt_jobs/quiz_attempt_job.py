from .base_attempt_job import BaseJob
from services.quizzes.quiz_evaluator import QuizEvaluator
from services.attempts.attempt_bundle import EvaluationBundle

class QuizAttemptJob(BaseJob):
    """Orchestrates quiz evaluation task as a celery job."""
    def execute(self, bundle: EvaluationBundle) -> dict:
        evaluator = QuizEvaluator()
        return evaluator.evaluate(bundle)