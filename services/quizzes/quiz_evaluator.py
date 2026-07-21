from copy import deepcopy

from .quiz_evaluator_schema import QuizEvaluationResponse, QuizQuestionEvaluation
from services.attempts.attempt_bundle import EvaluationBundle

class QuizEvaluator:
    """Evaluates a quiz attempt without modifying the original quiz content."""

    def evaluate(self, bundle: EvaluationBundle) -> dict:
        question_map = {
            question["question_id"]: question
            for question in bundle.question_paper["questions"]
        }

        answer_map = {
            answer["question_id"]: answer["answer"]
            for answer in bundle.submitted_answers
        }

        evaluations = []

        obtained_marks = 0

        marks = bundle.question_paper["marks_per_question"]

        negative = bundle.question_paper["negative_marking"]

        for question in bundle.question_paper["questions"]:
            submitted = answer_map.get(question["question_id"])

            if submitted is None:
                status = "unanswered"
                score = 0

            elif submitted == question["answer"]:
                status = "correct"
                score = marks

            else:
                status = "incorrect"
                score = -negative

            obtained_marks += score

            evaluations.append(
                QuizQuestionEvaluation(
                    question_id=question["question_id"],
                    question=question["question"],
                    obtained_marks=score,
                    maximum_marks=marks,
                    status=status,
                    user_answer=submitted,
                    correct_answer=question["answer"],
                    explanation=question["explanation"],
                )
            )

        return {
            "total_marks": len(evaluations) * marks,

            "obtained_marks": obtained_marks,

            "percentage": (
                obtained_marks /
                (len(evaluations) * marks)
            ) * 100,

            "evaluation": QuizEvaluationResponse(
                questions=evaluations
            ).model_dump(),
        }