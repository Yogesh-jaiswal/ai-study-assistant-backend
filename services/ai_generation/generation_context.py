from dataclasses import dataclass, field

@dataclass(slots=True)
class GenerationContext:
    """
    Carries every input required to generate AI content.

    The generation context describes *what* should be used during generation
    (e.g. notes, reference papers, exam blueprint) without containing the
    loaded resources themselves.

    It travels through the AI pipeline and keeps function signatures stable
    as new AI generation inputs are introduced.
    """

    note_ids: list[str]
    reference_ids: list[str] = field(default_factory=list)

    blueprint_slug: str | None = None