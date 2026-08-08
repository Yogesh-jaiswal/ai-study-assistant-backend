from typing import Any

from models.enums import EvaluationTypes

class QuestionNormalizer:
    """Normalizes quiz and exam questions into a common question format."""

    @classmethod
    def build(cls, content: dict, evaluation_type: EvaluationTypes) -> dict[str, Any]:
        """Builds a normalized question map for the given evaluation type."""
        NORMALIZER = {
            EvaluationTypes.QUIZ: cls._quiz_normalizer,
            EvaluationTypes.EXAM: cls._exam_normalizer
        }

        return NORMALIZER[evaluation_type](content)
    
    @staticmethod
    def _quiz_normalizer(content: dict) -> dict[str, Any]:
        """Normalizes quiz questions into the common question format."""
        question_map = {}

        for question in content["questions"]:
            question_id = question["question_id"]

            question_map[question_id] = {
                **question,
                "answer_type": "single_choice",
                "question_type": "MCQ",
            }

        return question_map
    
    @staticmethod
    def _exam_normalizer(content: dict) -> dict[str, Any]:
        """Normalizes exam questions using their group's question and answer types."""
        
        question_map = {}

        for section in content["sections"]:
            for group in section["question_groups"]:
                question_type = group["defaults"]["question_type"]
                answer_type = group["defaults"]["answer_type"]

                if group["questions"]:
                    for question in group["questions"]:
                        question_id = question["question_id"]

                        question_map[question_id] = {
                            **question,
                            "answer_type": answer_type,
                            "question_type": question_type,
                        }

                else:
                    for alt in group["alternatives"]:
                        for question in alt["questions"]:
                            question_id = question["question_id"]

                            question_map[question_id] = {
                                **question,
                                "answer_type": answer_type,
                                "question_type": question_type,
                            }

        return question_map