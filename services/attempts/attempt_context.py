from dataclasses import dataclass, field

@dataclass(slots=True)
class AttemptContext:
    """
    Carries every input required to evaluate AI content.

    The attempt context describes *what* should be used during evaluation
    (e.g. answers, generated papers) without containing the
    loaded resources themselves.

    It travels through the evaluation pipeline and keeps function signatures stable
    as new evaluation inputs are introduced.
    """

    content_id: str
    answers: list[dict]