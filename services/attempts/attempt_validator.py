from collections import Counter

from exceptions import (
    BadRequestError,
    ResourceNotFoundError
)
from models.enums import EvaluationTypes

from repositories.ai_content_repository import get_ai_content_by_content_id

from .question_normalizer import QuestionNormalizer

from .attempt_context import AttemptContext

ANSWER_TYPE_MAPPING = {
    "MCQ": str,
    "TrueFalse": bool,
    "SubjectiveShort": str,
    "Subjective": str,
    "FillBlank": str,
    "Numerical": (int, float),
    "MultiSelect": list,
    "DiagramQuestion": str,
    "Custom": (str, bool, int, float, list)
}


class AttemptValidator:
    """
    Validates every resource required for an evaluation request.
    """

    @classmethod
    def validate(cls, context: AttemptContext, notebook_id: str, user_id: str, evaluation_type: EvaluationTypes):

        ai_content = cls._validate_ai_content(
            notebook_id,
            context.content_id,
            user_id
        )

        question_map = QuestionNormalizer.build(ai_content.content, evaluation_type)

        if len(context.answers) > len(question_map):
            raise BadRequestError("Number of questions is greater than number of answers.")

        cls._validate_duplicate_questions(context.answers)

        cls._validate_answers(
            context.answers,
            question_map
        )

    @staticmethod
    def _validate_ai_content(
        notebook_id: str,
        content_id: str,
        user_id: str,
    ):

        ai_content = get_ai_content_by_content_id(
            notebook_id,
            user_id,
            content_id
        )

        if ai_content is None:
            raise ResourceNotFoundError(
                "AI content not found."
            )

        return ai_content

    @staticmethod
    def _validate_duplicate_questions(answers):

        ids = [answer["question_id"] for answer in answers]

        duplicates = [
            question_id
            for question_id, count in Counter(ids).items()
            if count > 1
        ]

        if duplicates:
            raise BadRequestError(
                "Duplicate question ids submitted."
            )

    @classmethod
    def _validate_answers(
        cls,
        answers,
        question_map,
    ):

        for submitted in answers:

            question = cls._validate_question_exists(
                submitted["question_id"],
                question_map
            )

            cls._validate_answer_type(
                question,
                submitted["answer"]
            )

            cls._validate_answer_value(
                question,
                submitted["answer"]
            )

    @staticmethod
    def _validate_question_exists(
        question_id,
        question_map,
    ):

        question = question_map.get(question_id)

        if question is None:
            raise BadRequestError(
                f"Unknown question id '{question_id}'."
            )

        return question

    @staticmethod
    def _validate_answer_type(
        question,
        answer,
    ):

        question_type = question["question_type"]

        if answer is None:
            return

        expected = ANSWER_TYPE_MAPPING.get(question_type)

        if expected is None:
            raise RuntimeError(
                f"Unsupported question type '{question_type}'."
            )

        if not isinstance(answer, expected):
            raise BadRequestError(
                f"Answer type does not match question type '{question_type}'."
            )

    @staticmethod
    def _validate_answer_value(
        question,
        answer,
    ):

        if answer is None:
            return

        question_type = question["question_type"]

        if question_type == "MCQ":

            options = {
                option["label"]
                for option in question["options"]
            }

            if answer not in options:
                raise BadRequestError(
                    "Submitted option is not present in the question."
                )

        elif question_type == "MultiSelect":

            options = {
                option["label"]
                for option in question["options"]
            }

            invalid = set(answer) - options

            if invalid:
                raise BadRequestError(
                    "Submitted options are invalid."
                )

        elif question_type in {
            "SubjectiveShort",
            "Subjective",
            "FillBlank",
            "DiagramQuestion"
        }:

            if not answer.strip():
                raise BadRequestError(
                    "Answer cannot be empty."
                )