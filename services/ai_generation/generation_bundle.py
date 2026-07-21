from dataclasses import dataclass
from validators.blueprint_schemas import BlueprintSchema


@dataclass(slots=True)
class GenerationBundle:
    """
    Contains all loaded resources required by an AI job.

    The bundle exposes strongly typed fields rather than generic mappings,
    making prompt construction explicit, type-safe, and easy to extend.
    """

    notes: str
    references: str | None = None
    blueprint: BlueprintSchema | None = None

    def to_prompt(self) -> str:
        sections = []

        sections.append(
            f"""
            ==============================
            KNOWLEDGE SOURCE (NOTES)
            ==============================

            This is the primary knowledge source.

            All generated content must be factually grounded in these notes.

            {self.notes.strip()}
        """.strip()
        )

        if self.references:
            sections.append(
                f"""
                ==============================
                REFERENCE PAPERS
                ==============================

                These papers are examples of formatting, presentation,
                question sequencing and writing style only.

                Do NOT copy questions verbatim.

                {self.references.strip()}
            """.strip()
            )

        if self.blueprint:
            sections.append(
                f"""
                ==============================
                EXAM BLUEPRINT
                ==============================

                This blueprint defines the examination structure.

                Follow every structural constraint exactly.

                {self.blueprint.model_dump_json(exclude_none=True, indent=2)}
            """.strip()
            )

        return "\n\n".join(sections)