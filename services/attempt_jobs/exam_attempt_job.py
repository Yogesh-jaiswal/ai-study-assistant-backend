from copy import deepcopy
from configs import get_settings

from .base_attempt_job import BaseJob
from services.exams.exam_evaluator import ExamEvaluator
from services.attempts.attempt_bundle import EvaluationBundle

class ExamAttemptJob(BaseJob):
    """Orchestrates quiz evaluation task as a celery job"""
    def execute(self, bundle: EvaluationBundle) -> dict:

        if get_settings().ENVIRONMENT == "testing":
            response = self._fake_evaluate(bundle)
        else:
            evaluator = ExamEvaluator()
            response = evaluator.evaluate(bundle)

        return self._merge_answers(
            bundle.question_paper,
            bundle.submitted_answers,
            response,
        )
        
    @staticmethod
    def _fake_evaluate(bundle: EvaluationBundle) -> dict:
        """
        Produce a deterministic evaluation without calling the AI model.

        Every question receives full marks together with a generic feedback
        message. Used only during testing.
        """

        sections = []

        for section in bundle.question_paper["sections"]:

            fake_section = {
                "section_name": section["section_name"],
                "questions": [],
            }

            for group in section["question_groups"]:

                question_lists = []

                if group["questions"]:
                    question_lists.append(group["questions"])
                else:
                    for alternative in group["alternatives"]:
                        question_lists.append(alternative["questions"])

                for questions in question_lists:
                    for question in questions:

                        fake_section["questions"].append(
                            {
                                "question_id": question["question_id"],
                                "obtained_marks": question["marks"],
                                "feedback": "Correct answer.",
                            }
                        )

            sections.append(fake_section)

        return {
            "overall_feedback": "Excellent performance.",
            "sections": sections,
        }

    def _merge_answers(
        self,
        question_paper: dict,
        submitted_answers: list[dict],
        evaluation: dict,
    ) -> dict:
        """
        Merge:

        - original question paper
        - submitted answers
        - AI evaluation

        into a single evaluation blob.

        Returns:
            Fully merged paper ready for storage.
        """

        merged = deepcopy(question_paper)

        answer_map = {
            answer["question_id"]: answer["answer"]
            for answer in submitted_answers
        }

        evaluation_map = {}

        for section in evaluation["sections"]:
            for question in section["questions"]:
                evaluation_map[
                    question["question_id"]
                ] = question

        total_obtained = 0

        for section in merged["sections"]:

            section_obtained = 0

            for group in section["question_groups"]:

                if group["questions"]:

                    score = self._merge_question_list(
                        questions=group["questions"],
                        answer_map=answer_map,
                        evaluation_map=evaluation_map
                    )

                else:

                    score = 0

                    for alt in group["alternatives"]:

                        score += self._merge_question_list(
                            questions=alt["questions"],
                            answer_map=answer_map,
                            evaluation_map=evaluation_map
                        )

                group["obtained_marks"] = score

                section_obtained += score

            section["obtained_marks"] = section_obtained

            total_obtained += section_obtained

        merged["overall_feedback"] = evaluation["overall_feedback"]

        return {
            "total_marks": merged["total_marks"],
            "obtained_marks": total_obtained,
            "percentage": (
                total_obtained /
                merged["total_marks"]
            ) * 100,
            "evaluation": merged,
        }
    
    @staticmethod
    def _merge_question_list(
        questions,
        answer_map,
        evaluation_map
    ):
        obtained = 0

        for question in questions:

            question_id = question["question_id"]

            question["user_answer"] = answer_map.get(
                question_id
            )

            evaluation = evaluation_map[question_id]

            question["feedback"] = evaluation["feedback"]

            question["obtained_marks"] = evaluation[
                "obtained_marks"
            ]

            obtained += evaluation["obtained_marks"]

        return obtained