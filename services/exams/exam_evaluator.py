from configs import get_settings

from services.ai.engine import AIEngine

from .exam_evaluator_prompt import create_exam_evaluator_prompt
from .exam_evaluator_schema import ExamEvaluationResponse

from services.attempts.attempt_bundle import EvaluationBundle


class ExamEvaluator:
    """Evaluates student answers for an exam using the AI engine based on the provided resources and answers."""

    def __init__(self):
        self.model = AIEngine(get_settings().AI_MODEL)

    def evaluate(self, bundle: EvaluationBundle) -> dict:
        prompt = create_exam_evaluator_prompt(bundle.to_prompt())

        return self.model.complete(prompt, ExamEvaluationResponse)