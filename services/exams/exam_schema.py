from typing import Optional

from pydantic import BaseModel, Field

class Option(BaseModel):
    """
    A single answer option for an objective question.
    """

    label: str = Field(
        description="Display label such as A, B, C, D."
    )

    text: str = Field(
        description="Text shown to the student."
    )

class Question(BaseModel):
    """
    Represents a single examination question.

    The structural properties such as marks, answer type,
    negative marking, and selection rules are defined by the
    blueprint. This schema contains only AI-generated content.
    """

    question_label: str = Field(
        description="Display identifier such as Q1, Q12, 1(a), or Essay 2."
    )

    question: str = Field(
        description="The complete question text presented to the student."
    )

    options: Optional[list[Option]] = Field(
        default=None,
        description="Answer options for objective questions. Omitted for subjective, numerical, drawing, or essay questions."
    )

class Alternative(BaseModel):
    """
    Represents a single alterantive for or type questions.
    """
    title: str = Field(
        description="Title for the alterantive questions."
    )

    questions: list[Question] = Field (
        min_length=2,
        description="Questions inside the alteranatives."
    )

class QuestionGroup(BaseModel):
    """
    A logical group of related questions.

    Examples include:
    - Reading comprehension passage
    - Case study
    - Numerical data set
    - Diagram-based questions
    """

    group_title: str

    shared_material: Optional[str] = Field(
        default=None,
        description="Common material shared by all questions in this group."
    )

    questions: list[Question] | None = None

    alternatives: list[Alternative] | None = None

class Section(BaseModel):
    """
    Represents a major examination section such as Physics,
    Mathematics, or Reading Comprehension.
    """

    section_name: str

    question_groups: list[QuestionGroup]

class ExamResponse(BaseModel):
    """
    Complete AI-generated examination paper.

    The examination structure follows the supplied blueprint,
    while this response contains only generated question content.
    """

    title: str

    sections: list[Section]