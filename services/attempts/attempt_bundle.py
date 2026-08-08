from dataclasses import dataclass

@dataclass(slots=True)
class EvaluationBundle:
    """
    Contains all loaded resources required by an AI job.

    The bundle exposes strongly typed fields rather than generic mappings,
    making prompt construction explicit, type-safe, and easy to extend.
    """

    question_paper: dict
    submitted_answers: list[dict]

    def to_prompt(self) -> str:
        sections = []

        sections.append(
            f"""
            ==============================
            QUSETION PAPER
            ==============================

            This is the question paper.

            All the submitted answers have a matching question in it by the question id.

            {self.question_paper}
        """.strip()
        )

        
        sections.append(
            f"""
            ==============================
            SUBMITTED ANSWERS
            ==============================

            These are the submitted answers with a valid question id.

            {self.submitted_answers}
        """.strip()
        )

        return "\n\n".join(sections)