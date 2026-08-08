"""
Module for registering attempt jobs with their corresponding evaluation types.
"""

from models.enums import EvaluationTypes

from .quiz_attempt_job import QuizAttemptJob
from .exam_attempt_job import ExamAttemptJob

ATTEMPT_JOB_REGISTRY = {
    EvaluationTypes.QUIZ: QuizAttemptJob(),
    EvaluationTypes.EXAM: ExamAttemptJob()
}