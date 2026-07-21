from copy import deepcopy
from uuid import uuid4

from faker import Faker

from configs import get_settings

from .base_job import BaseJob
from services.exams.exam_generator import ExamGenerator
from services.ai_generation.generation_bundle import GenerationBundle

fake = Faker()


class ExamGenerationJob(BaseJob):
    """Orchestrates exam generation."""

    def execute(
        self,
        generation_options: dict,
        bundle: GenerationBundle,
    ) -> dict:

        if get_settings().ENVIRONMENT == "testing":
            return self._fake_execute(
                generation_options,
                bundle,
            )

        resources = bundle.to_prompt()

        generator = ExamGenerator()

        response = generator.generate(
            resources,
            generation_options,
        )

        merged = deepcopy(bundle.blueprint.model_dump())

        merged["title"] = response["title"]
        merged["difficulty"] = generation_options["difficulty"]

        for bp_section, ai_section in zip(
            merged["sections"],
            response["sections"],
        ):
            for bp_group, ai_group in zip(
                bp_section["question_groups"],
                ai_section["question_groups"],
            ):
                bp_group["shared_material"] = ai_group["shared_material"]

                negative = bp_group["defaults"]["negative_marking"]

                if ai_group["questions"]:

                    self._apply_question_metadata(
                        ai_group["questions"],
                        bp_group["parts"],
                        negative,
                    )

                    bp_group["questions"] = ai_group["questions"]

                else:

                    for bp_alt, ai_alt in zip(
                        bp_group["alternatives"],
                        ai_group["alternatives"],
                    ):

                        self._apply_question_metadata(
                            ai_alt["questions"],
                            bp_alt["parts"],
                            negative,
                        )

                        bp_alt["questions"] = ai_alt["questions"]

        return merged

    @staticmethod
    def _fake_execute(
        generation_options: dict,
        bundle: GenerationBundle,
    ) -> dict:

        exam = deepcopy(bundle.blueprint.model_dump())

        exam["title"] = fake.sentence(nb_words=4)
        exam["difficulty"] = generation_options["difficulty"]

        for section in exam["sections"]:

            for group in section["question_groups"]:

                group["shared_material"] = fake.paragraph()

                negative = group["defaults"]["negative_marking"]
                answer_type = group["defaults"]["answer_type"]

                if group["alternatives"]:

                    for alternative in group["alternatives"]:

                        alternative["questions"] = (
                            ExamGenerationJob._build_questions(
                                alternative["parts"],
                                answer_type,
                                negative,
                            )
                        )

                else:

                    group["questions"] = (
                        ExamGenerationJob._build_questions(
                            group["parts"],
                            answer_type,
                            negative,
                        )
                    )

        return exam

    @staticmethod
    def _build_questions(
        parts,
        answer_type,
        negative_marking,
    ):

        questions = []
        counter = 1

        for part in parts:

            for _ in range(part["count"]):

                question = {
                    "question_id": str(uuid4()),
                    "question_label": f"Q{counter}",
                    "question": fake.sentence(nb_words=12),
                    "marks": part["marks"],
                    "negative_marking": negative_marking,
                }

                if answer_type in (
                    "single_choice",
                    "multiple_choice",
                ):
                    question["options"] = (
                        ExamGenerationJob._build_options()
                    )

                questions.append(question)
                counter += 1

        return questions

    @staticmethod
    def _build_options():

        return [
            {"label": "A", "text": fake.word()},
            {"label": "B", "text": fake.word()},
            {"label": "C", "text": fake.word()},
            {"label": "D", "text": fake.word()},
        ]

    @staticmethod
    def _apply_question_metadata(
        questions: list[dict],
        parts: list[dict],
        negative_marking: int,
    ):
        index = 0

        for part in parts:

            marks = part["marks"]

            for _ in range(part["count"]):
                questions[index]["marks"] = marks
                questions[index]["negative_marking"] = negative_marking
                questions[index]["question_id"] = str(uuid4())
                index += 1